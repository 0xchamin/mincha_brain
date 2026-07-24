# link-agents.ps1 - Windows (PowerShell)
# One canonical contract (AGENTS.md), symlinked to the pointer paths some harnesses expect.
# Run ONCE per clone. The links are git-ignored, so nothing tool-specific is ever maintained.
#
#   Copilot CLI, Codex, Cursor  -> read AGENTS.md natively (no link needed)
#   Claude Code                 -> CLAUDE.md
#   GitHub Copilot (IDE/agent)  -> .github/copilot-instructions.md
#
# Symlinks on Windows require Developer Mode (Settings > For developers) OR an elevated shell.
# Usage:  .\link-agents.ps1
$ErrorActionPreference = 'Stop'
Set-Location -Path $PSScriptRoot

$pointerText = "Read AGENTS.md - it is the single source of truth for every agent harness."

function New-Link($link, $target) {
    if (Test-Path $link) {
        $item = Get-Item $link -Force
        $isSymlink = $item.Attributes -band [IO.FileAttributes]::ReparsePoint
        $isPointer = (-not $isSymlink) -and ((Get-Content $link -Raw -ErrorAction SilentlyContinue).Trim() -eq $pointerText)
        if (-not ($isSymlink -or $isPointer)) {
            Write-Host "  SKIP     $link already exists and is NOT a generated link/pointer - leaving it untouched."
            return
        }
        Remove-Item $link -Force
    }
    try {
        New-Item -ItemType SymbolicLink -Path $link -Target $target -Force | Out-Null
        Write-Host "  symlink  $link -> $target"
    } catch {
        # Fallback when symlinks aren't permitted: a tiny pointer file (still git-ignored).
        # NOTE: this is a POINTER, not a live link - it will not track edits to AGENTS.md.
        # Enable Developer Mode and re-run to get a real symlink.
        $pointerText | Set-Content -Path $link -Encoding utf8
        Write-Host "  POINTER  $link (symlink not permitted; wrote a static one-line pointer - NOT a live link)"
    }
}

New-Link 'CLAUDE.md' 'AGENTS.md'
New-Item -ItemType Directory -Force -Path '.github' | Out-Null
New-Link '.github\copilot-instructions.md' '..\AGENTS.md'

Write-Host "Codex, Cursor and Copilot CLI read AGENTS.md natively - no link needed."
