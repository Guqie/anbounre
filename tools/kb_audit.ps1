[CmdletBinding()]
param(
    [string]$Root = ".",
    [string]$OutFile = "",
    [string]$CsvFile = ""
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Get-RelativePath {
    param(
        [string]$BasePath,
        [string]$FullPath
    )

    $base = (Resolve-Path $BasePath).Path
    $full = (Resolve-Path $FullPath).Path
    $baseUri = New-Object System.Uri(($base.TrimEnd('\') + '\'))
    $fullUri = New-Object System.Uri($full)
    $rel = $baseUri.MakeRelativeUri($fullUri).ToString()
    return [System.Uri]::UnescapeDataString($rel).Replace('/', '\')
}

$excludeDirs = @(
    ".git",
    ".obsidian",
    ".spec-workflow",
    ".trae",
    ".claude",
    "node_modules",
    "templates",
    "tools"
)

$typePrefix = ([string][char]0x7C7B) + ([string][char]0x578B) + "/"
$statusPrefix = ([string][char]0x72B6) + ([string][char]0x6001) + "/"

$files = Get-ChildItem -Path $Root -Recurse -File -Filter "*.md" | Where-Object {
    $path = $_.FullName
    foreach ($dir in $excludeDirs) {
        if ($path -match [Regex]::Escape("\$dir\")) {
            return $false
        }
    }
    return $true
}

$docs = @()
$stemIndex = @{}
$pathIndex = @{}

foreach ($f in $files) {
    try {
        $content = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
    }
    catch {
        $content = ""
    }
    if ($null -eq $content) {
        $content = ""
    }
    $relPath = Get-RelativePath -BasePath $Root -FullPath $f.FullName
    $relNoExt = [System.IO.Path]::ChangeExtension($relPath, $null).TrimEnd('.')
    $stem = [System.IO.Path]::GetFileNameWithoutExtension($f.Name)

    $fmMatch = [Regex]::Match($content, "(?s)^---\r?\n(.*?)\r?\n---\r?\n")
    $hasFrontmatter = $fmMatch.Success
    $frontmatter = if ($hasFrontmatter) { $fmMatch.Groups[1].Value } else { "" }

    $hasTags = $frontmatter -match "(?m)^tags\s*:"
    $hasTypeTag = $frontmatter.Contains($typePrefix)
    $hasStatusTag = $frontmatter.Contains($statusPrefix)

    $links = @()
    $linkMatches = [Regex]::Matches($content, "\[\[([^\]|#]+)")
    foreach ($m in $linkMatches) {
        $target = $m.Groups[1].Value.Trim().Replace('/', '\')
        if ($target.Length -gt 0) {
            $links += $target
        }
    }

    $doc = [PSCustomObject]@{
        RelativePath   = $relPath
        RelativeNoExt  = $relNoExt
        Stem           = $stem
        HasFrontmatter = $hasFrontmatter
        HasTags        = $hasTags
        HasTypeTag     = $hasTypeTag
        HasStatusTag   = $hasStatusTag
        Links          = $links
    }
    $docs += $doc

    if (-not $stemIndex.ContainsKey($stem)) {
        $stemIndex[$stem] = @()
    }
    $stemIndex[$stem] += $relPath
    $pathIndex[$relNoExt] = $true
}

$inbound = @{}
foreach ($d in $docs) {
    $inbound[$d.RelativePath] = 0
}

foreach ($d in $docs) {
    foreach ($targetRaw in $d.Links) {
        $target = $targetRaw.Trim()
        $targetNoExt = [System.IO.Path]::ChangeExtension($target, $null).TrimEnd('.')
        if ([string]::IsNullOrWhiteSpace($targetNoExt)) {
            continue
        }

        if ($pathIndex.ContainsKey($targetNoExt)) {
            $match = $docs | Where-Object { $_.RelativeNoExt -eq $targetNoExt } | Select-Object -First 1
            if ($null -ne $match) {
                $inbound[$match.RelativePath]++
            }
            continue
        }

        $targetStem = Split-Path $targetNoExt -Leaf
        if ($stemIndex.ContainsKey($targetStem)) {
            foreach ($p in $stemIndex[$targetStem]) {
                $inbound[$p]++
            }
        }
    }
}

$missingFrontmatter = $docs | Where-Object { -not $_.HasFrontmatter }
$missingTags = $docs | Where-Object { $_.HasFrontmatter -and -not $_.HasTags }
$missingType = $docs | Where-Object { $_.HasFrontmatter -and -not $_.HasTypeTag }
$missingStatus = $docs | Where-Object { $_.HasFrontmatter -and -not $_.HasStatusTag }
$orphanDocs = $docs | Where-Object {
    $isSystem = $_.Stem -like "_MOC-*" -or $_.Stem -in @("README", "CLAUDE")
    (-not $isSystem) -and ($inbound[$_.RelativePath] -eq 0)
}

if ([string]::IsNullOrWhiteSpace($OutFile)) {
    $OutFile = Join-Path $Root ("kb-audit-report-" + (Get-Date -Format "yyyy-MM-dd") + ".md")
}

$lines = @()
$lines += "# Knowledge Base Audit Report"
$lines += ""
$lines += "- Generated at: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")"
$lines += "- Scan root: $((Resolve-Path $Root).Path)"
$lines += "- Markdown files: $($docs.Count)"
$lines += ""
$lines += "## Summary"
$lines += ""
$lines += "| Metric | Count |"
$lines += "|---|---:|"
$lines += "| Missing frontmatter | $($missingFrontmatter.Count) |"
$lines += "| Missing tags in frontmatter | $($missingTags.Count) |"
$lines += "| Missing type tag | $($missingType.Count) |"
$lines += "| Missing status tag | $($missingStatus.Count) |"
$lines += "| Orphan docs (no inbound links) | $($orphanDocs.Count) |"
$lines += ""

function Add-Top {
    param(
        [string]$Title,
        [array]$Items,
        [int]$Top = 20
    )

    $script:lines += "## $Title"
    $script:lines += ""
    if ($Items.Count -eq 0) {
        $script:lines += "- none"
        $script:lines += ""
        return
    }

    $count = [Math]::Min($Top, $Items.Count)
    for ($i = 0; $i -lt $count; $i++) {
        $script:lines += "- $($Items[$i].RelativePath)"
    }
    if ($Items.Count -gt $Top) {
        $script:lines += "- ... and $($Items.Count - $Top) more"
    }
    $script:lines += ""
}

Add-Top -Title "Missing frontmatter (top 20)" -Items $missingFrontmatter
Add-Top -Title "Missing tags (top 20)" -Items $missingTags
Add-Top -Title "Missing type tag (top 20)" -Items $missingType
Add-Top -Title "Missing status tag (top 20)" -Items $missingStatus
Add-Top -Title "Orphan docs (top 20)" -Items $orphanDocs

$lines += "## Suggested next actions"
$lines += ""
$lines += "1. Fix frontmatter first, then add ``类型/`` and ``状态/`` tags."
$lines += "2. Link orphan docs through MOC pages."
$lines += "3. Run this audit weekly and track trend."

# --- CSV trend tracking ---
if ([string]::IsNullOrWhiteSpace($CsvFile)) {
    $CsvFile = Join-Path $Root "tools/kb-audit-history.csv"
}

$today = Get-Date -Format "yyyy-MM-dd"
$fmCoverage = if ($docs.Count -gt 0) {
    [math]::Round(($docs.Count - $missingFrontmatter.Count) / $docs.Count * 100, 1)
} else { 0 }
$orphanPct = if ($docs.Count -gt 0) {
    [math]::Round($orphanDocs.Count / $docs.Count * 100, 1)
} else { 0 }

$csvRow = "$today,$($docs.Count),$($missingFrontmatter.Count),$($missingTags.Count)," +
          "$($missingType.Count),$($missingStatus.Count),$($orphanDocs.Count),$fmCoverage,$orphanPct"

if (-not (Test-Path $CsvFile)) {
    $csvHeader = "date,total_docs,missing_fm,missing_tags,missing_type,missing_status,orphans,fm_coverage_pct,orphan_pct"
    [System.IO.File]::WriteAllText($CsvFile, $csvHeader + [Environment]::NewLine, [System.Text.Encoding]::UTF8)
}
[System.IO.File]::AppendAllText($CsvFile, $csvRow + [Environment]::NewLine, [System.Text.Encoding]::UTF8)

# --- Week-over-week comparison ---
$csvLines = [System.IO.File]::ReadAllLines($CsvFile, [System.Text.Encoding]::UTF8) | Where-Object { $_ -notmatch "^date," -and $_.Trim().Length -gt 0 }

if ($csvLines.Count -ge 2) {
    $prev = $csvLines[-2].Split(",")
    $curr = $csvLines[-1].Split(",")

    $lines += ""
    $lines += "## Week-over-week comparison"
    $lines += ""
    $lines += "| Metric | Previous ($($prev[0])) | Current ($($curr[0])) | Delta |"
    $lines += "|---|---:|---:|---:|"

    $metricNames = @("Total docs", "Missing FM", "Missing tags", "Missing type", "Missing status", "Orphans", "FM coverage %", "Orphan %")
    for ($i = 0; $i -lt $metricNames.Count; $i++) {
        $pVal = [double]$prev[$i + 1]
        $cVal = [double]$curr[$i + 1]
        $delta = $cVal - $pVal
        $sign = if ($delta -gt 0) { "+" } elseif ($delta -lt 0) { "" } else { "" }
        $lines += "| $($metricNames[$i]) | $pVal | $cVal | $sign$delta |"
    }
    $lines += ""
}

[System.IO.File]::WriteAllText($OutFile, ($lines -join [Environment]::NewLine), [System.Text.Encoding]::UTF8)
Write-Output "Report generated: $OutFile"
Write-Output "CSV history updated: $CsvFile"
