# NBA Foul Analysis

This repository contains a work-in-progress mini-project analysing foul-calling behavior in the NBA using play-by-play data from multiple seasons. The project includes data processing, exploratory analysis, and deeper analysis.


## Project Status

- **Status:** In Progress  
- **Current Phase:** Exploratory Data Analysis (EDA)
- **Scope:** Multi-season analysis across all 30 NBA teams


## Key Research Questions

### Core Questions:
- Are fewer fouls called in the final 2 minutes of a close game (score margin ≤ 5) compared to the rest of the game?
- Are fewer shooting fouls called late in close games?
- Do different types of fouls (personal, offensive, technical) change in frequency near the end of the game?
- Does the home team or visitor team commit fewer fouls?

### Overtime Analysis:
- What is the distribution of fouls in overtime periods?
- How do foul rates in overtime compare to regular time?
- How do foul frequencies and types differ in games that go to overtime vs those that do not?

### Foul Rates & Game Context:
- Compare foul rates between:
  - The last 2 minutes of the 4th quarter in close games
  - The rest of regulation
- Compute fouls per minute in each period
- How many of these fouls occurred in "close games" (score margin ≤ 5)?


## Planned Segmentations

- Game closeness: Close games (score margin ≤ 5) vs blowouts
- Foul type: Personal vs offensive vs technical vs flagrant
- Game phase: Early game vs late game
- Team role: Home team vs visitor team
- Win status (planned): Does the losing team commit more fouls?


## Additional Exploratory Questions

- Compare technical vs personal foul rates by score margin
- Check how score margin affects foul frequency in the last 2 minutes
- Assess whether foul calls changed in the absence of crowd pressure (e.g., during the 2019–2020 NBA bubble)
  - Compare pre-bubble vs bubble period data


## Current Progress

- Data collected using `nba_api` (play-by-play and game metadata)
- Extracted foul events across multiple seasons
- Cleaned and structured data to include time, type, and sscore margin
- Ongoing: EDA


## Next Steps

- Compare foul behavior between seasons (including bubble season)
- Visualise foul types by period, margin, and team
- Evaluate significance of observed patterns


This project is an independent mini-project aimed at exploring patterns in NBA foul data using real-world multi-season data.
