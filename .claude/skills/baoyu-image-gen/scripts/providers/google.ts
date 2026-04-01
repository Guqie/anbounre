import path from "node:path";
import { readFile } from "node:fs/promises";
import { execSync } from "node:child_process";
import type { CliArgs } from "../types";

const GOOGLE_MULTIMODAL_MODELS = [
  "gemini-3-pro-image-preview",
  "gemini-3-flash-preview",
  "gemini-3.1-flash-image-preview",
];
const GOOGLE_IMAGEN_MODELS = [
  "imagen-3.0-generate-002",
  "imagen-3.0-generate-001",
];

export function getDefaultModel(): string {
  return process.env.GOOGLE_IMAGE_MODEL || "gemini-3-pro-image-preview";
}

function normalizeGoogleModelId(model: string): string {
  return model.startsWith("models/") ? model.slice("models/".length) : model;
}

function isGoogleMultimodal(model: string): boolean {
  const normalized = normalizeGoogleModelId(model);
  return GOOGLE_MULTIMODAL_MODELS.some((m) => normalized.includes(m));
}

function isGoogleImagen(model: string): boolean {
  const normalized = normalizeGoogleModelId(model);
  return GOOGLE_IMAGEN_MODELS.some((m) => normalized.includes(m));
}

function getGoogleApiKey(): string | null {
  return process.env.GOOGLE_API_KEY || process.env.GEMINI_API_KEY || null;
}

function getGoogleImageSize(args: CliArgs): "1K" | "2K" | "4K" {
  if (args.imageSize) return args.imageSize as "1K" | "2K" | "4K";
  return args.quality === "2k" ? "2K" : "1K";
}

function getGoogleBaseUrl(): string {
  if (process.env.GOOGLE_API_BASE) {
    return process.env.GOOGLE_API_BASE.replace(/\/+$/g, "");
  }
  if (process.env.GOOGLE_BASE_URL) {
    return process.env.GOOGLE_BASE_URL.replace(/\/+$/g, "");
  }
  return "https://generativelanguage.googleapis.com";
}

function buildGoogleUrl(pathname: string): string {
  const base = getGoogleBaseUrl();
  // If base URL already includes full path (like third-party proxies often do), use it directly
  // Third-party APIs like newcli often use: https://code.newcli.com/gemini/v1beta/...
  if (base.includes("/v1beta") || base.includes("/v1")) {
     // For custom endpoints that might already include version
     return `${base}/${pathname.replace(/^\/+/, "")}`;
  }
  
  return `${base}/v1beta/${pathname.replace(/^\/+/, "")}`;
}

function toModelPath(model: string): string {
  const modelId = normalizeGoogleModelId(model);
  return `models/${modelId}`;
}

function getHttpProxy(): string | null {
  return (
    process.env.https_proxy ||
    process.env.HTTPS_PROXY ||
    process.env.http_proxy ||
    process.env.HTTP_PROXY ||
    process.env.ALL_PROXY ||
    null
  );
}

async function postGoogleJsonViaCurl<T>(
  url: string,
  apiKey: string,
  body: unknown,
): Promise<T> {
  const proxy = getHttpProxy();
  const bodyStr = JSON.stringify(body);
  const proxyArgs = proxy ? `-x "${proxy}"` : "";

  const result = execSync(
    `curl -s --connect-timeout 30 --max-time 300 ${proxyArgs} "${url}" -H "Content-Type: application/json" -H "x-goog-api-key: ${apiKey}" -H "Authorization: Bearer ${apiKey}" -d @-`,
    { input: bodyStr, maxBuffer: 100 * 1024 * 1024, timeout: 310000 },
  );

  const parsed = JSON.parse(result.toString()) as any;
  if (parsed.error) {
    throw new Error(
      `Google API error (${parsed.error.code}): ${parsed.error.message}`,
    );
  }
  return parsed as T;
}

async function postGoogleJsonViaFetch<T>(
  url: string,
  apiKey: string,
  body: unknown,
): Promise<T> {
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-goog-api-key": apiKey,
      "Authorization": `Bearer ${apiKey}`,
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Google API error (${res.status}): ${err}`);
  }

  return (await res.json()) as T;
}

async function postGoogleJson<T>(pathname: string, body: unknown): Promise<T> {
  const apiKey = getGoogleApiKey();
  if (!apiKey) throw new Error("GOOGLE_API_KEY or GEMINI_API_KEY is required");

  const url = buildGoogleUrl(pathname);
  const proxy = getHttpProxy();

  // When an HTTP proxy is detected, use curl instead of fetch.
  // Bun's fetch has a known issue where long-lived connections through
  // HTTP proxies get their sockets closed unexpectedly, causing image
  // generation requests to fail with "socket connection was closed
  // unexpectedly". Using curl as the HTTP client works around this.
  
  // Many third-party proxies require the API key in the URL query parameter
  // in addition to (or instead of) the x-goog-api-key header.
  const urlWithKey = url.includes("?") 
    ? `${url}&key=${apiKey}` 
    : `${url}?key=${apiKey}`;
    
  if (proxy) {
    return postGoogleJsonViaCurl<T>(urlWithKey, apiKey, body);
  }

  return postGoogleJsonViaFetch<T>(urlWithKey, apiKey, body);
}

function buildPromptWithAspect(
  prompt: string,
  ar: string | null,
  quality: CliArgs["quality"],
): string {
  let result = prompt;
  if (ar) {
    result += ` Aspect ratio: ${ar}.`;
  }
  if (quality === "2k") {
    result += " High resolution 2048px.";
  }
  return result;
}

function addAspectRatioToPrompt(prompt: string, ar: string | null): string {
  if (!ar) return prompt;
  return `${prompt} Aspect ratio: ${ar}.`;
}

async function readImageAsBase64(
  p: string,
): Promise<{ data: string; mimeType: string }> {
  const buf = await readFile(p);
  const ext = path.extname(p).toLowerCase();
  let mimeType = "image/png";
  if (ext === ".jpg" || ext === ".jpeg") mimeType = "image/jpeg";
  else if (ext === ".gif") mimeType = "image/gif";
  else if (ext === ".webp") mimeType = "image/webp";
  return { data: buf.toString("base64"), mimeType };
}

function extractInlineImageData(response: {
  candidates?: Array<{
    content?: { parts?: Array<{ inlineData?: { data?: string } }> };
  }>;
}): string | null {
  for (const candidate of response.candidates || []) {
    for (const part of candidate.content?.parts || []) {
      const data = part.inlineData?.data;
      if (typeof data === "string" && data.length > 0) return data;
    }
  }
  return null;
}

function extractPredictedImageData(response: {
  predictions?: Array<any>;
  generatedImages?: Array<any>;
}): string | null {
  const candidates = [
    ...(response.predictions || []),
    ...(response.generatedImages || []),
  ];
  for (const candidate of candidates) {
    if (!candidate || typeof candidate !== "object") continue;
    if (typeof candidate.imageBytes === "string") return candidate.imageBytes;
    if (typeof candidate.bytesBase64Encoded === "string")
      return candidate.bytesBase64Encoded;
    if (typeof candidate.data === "string") return candidate.data;
    const image = candidate.image;
    if (image && typeof image === "object") {
      if (typeof image.imageBytes === "string") return image.imageBytes;
      if (typeof image.bytesBase64Encoded === "string")
        return image.bytesBase64Encoded;
      if (typeof image.data === "string") return image.data;
    }
  }
  return null;
}

async function generateWithGemini(
  prompt: string,
  model: string,
  args: CliArgs,
): Promise<Uint8Array> {
  const promptWithAspect = addAspectRatioToPrompt(prompt, args.aspectRatio);
  const parts: Array<{
    text?: string;
    inlineData?: { data: string; mimeType: string };
  }> = [];
  for (const refPath of args.referenceImages) {
    const { data, mimeType } = await readImageAsBase64(refPath);
    parts.push({ inlineData: { data, mimeType } });
  }
  parts.push({ text: promptWithAspect });

  const imageConfig: { imageSize: "1K" | "2K" | "4K" } = {
    imageSize: getGoogleImageSize(args),
  };

  console.log("Generating image with Gemini...", imageConfig);
  const response = await postGoogleJson<{
    candidates?: Array<{
      content?: { parts?: Array<{ inlineData?: { data?: string } }> };
    }>;
  }>(`${toModelPath(model)}:generateContent`, {
    contents: [
      {
        role: "user",
        parts,
      },
    ],
    generationConfig: {
      responseModalities: ["IMAGE"],
      imageConfig,
    },
  });
  console.log("Generation completed.");

  const imageData = extractInlineImageData(response);
  if (imageData) return Uint8Array.from(Buffer.from(imageData, "base64"));

  throw new Error("No image in response");
}

async function generateWithImagen(
  prompt: string,
  model: string,
  args: CliArgs,
): Promise<Uint8Array> {
  const fullPrompt = buildPromptWithAspect(
    prompt,
    args.aspectRatio,
    args.quality,
  );
  const imageSize = getGoogleImageSize(args);
  if (imageSize === "4K") {
    console.error(
      "Warning: Imagen models do not support 4K imageSize, using 2K instead.",
    );
  }

  const parameters: Record<string, unknown> = {
    sampleCount: args.n,
  };
  if (args.aspectRatio) {
    parameters.aspectRatio = args.aspectRatio;
  }
  if (imageSize === "1K" || imageSize === "2K") {
    parameters.imageSize = imageSize;
  } else {
    parameters.imageSize = "2K";
  }

  const response = await postGoogleJson<{
    predictions?: Array<any>;
    generatedImages?: Array<any>;
  }>(`${toModelPath(model)}:predict`, {
    instances: [
      {
        prompt: fullPrompt,
      },
    ],
    parameters,
  });

  const imageData = extractPredictedImageData(response);
  if (imageData) return Uint8Array.from(Buffer.from(imageData, "base64"));

  throw new Error("No image in response");
}

export async function generateImage(
  prompt: string,
  model: string,
  args: CliArgs,
): Promise<Uint8Array> {
  if (isGoogleImagen(model)) {
    if (args.referenceImages.length > 0) {
      throw new Error(
        "Reference images are not supported with Imagen models. Use gemini-3-pro-image-preview, gemini-3-flash-preview, or gemini-3.1-flash-image-preview.",
      );
    }
    return generateWithImagen(prompt, model, args);
  }

  if (!isGoogleMultimodal(model) && args.referenceImages.length > 0) {
    throw new Error(
      "Reference images are only supported with Gemini multimodal models. Use gemini-3-pro-image-preview, gemini-3-flash-preview, or gemini-3.1-flash-image-preview.",
    );
  }

  return generateWithGemini(prompt, model, args);
}
