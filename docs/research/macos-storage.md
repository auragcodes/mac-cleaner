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

## Candidate Cleanup Categories

- Caches: I believe, we will have to investigate it when running the application and not just completely deleting all of it, as some caches are important. [INVESTIGATE]

- Logs: Similiar as cache, it will depend for each log files and we can't blindly delete all of it. [INVESTIGATE]

- Browser Cache/Service-Worker Data: Should be safe to touch it, as at worst it will log you out of some sites or reset offline app content. Although, it is not something preferred, overally it should be more safer than others. [INVESTIGATE]

- Temporary Files: Should be safe as they are temporary. [INVESTIGATE]

- Persistent Application Data: Should NOT be touched unless we are extremely carefull going through it. [DO NOT TOUCH]

- User Data: Same as persistent application data, it shouldn't be touched careless unless following some strict protocol. [DO NOT TOUCH]

## Initial Feature

The first version of this cleaner should ask for a directory then scan it and report and files/directories that match cleaning categories, including their sizes, BUT do not delete anything.

The main purpose is to understand what we are finding and determine what is safe to investigate and eventually delete, rather than outright deleting things from the get-go.

## **Candidate Information**

Information one reported candidate should contain:

- Path

- Size

- Category

- Safety Classification

- Reason - why the candidate received its safety classification