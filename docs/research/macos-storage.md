# macOS Storage Research

## Source

Apple - Free up storage space on MAC
https://support.apple.com/en-in/guide/mac-help/mchl3d437fbc/mac

## Findings

So, macOS's "System Data" is a broad category containing system and application related files that don't fit into the other storage categories.

Examples include:

- Logs
- Caches
- VM Files
- Temporary Files
- Runtime System Resources
- Application Support Files
- Fonts
- Other system-related resources

## Initial Observation

"System Data" doesn't appear to represent one specific directory which we can just simply delete.
So this project needs to identify which files and directories that can be safely managed rather than deleting the whole "System Data".