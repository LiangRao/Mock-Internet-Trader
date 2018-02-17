Project Specification Feedback
==================

### The product backlog (9/10)
Your list of specification is good. One thing you should include is a cost estimate for each feature, in hours. If the cost estimate is more than 5 or 8 hours, you should consider breaking the feature into smaller work units to improve your ability to track progress on it. Additionally, a spreadsheet-like format is easier to read for backlogs, rather than prose or bulleted lists.  You could also explore existing online tools for generating and tracking work on a project. Finally, you might want to include how you will integrate the APIs (which part of the functionality uses what). This will make it more clear as to who needs to figure out how to interact with your APIs. 

### Data models (9/10)
It is unclear what the relationship between a Game and a Player is. In the specification, you wrote that a player can join multiple games, and will have a balance and set of stocks in each game. However, in your models, the remaining_balance and stocks are stored in the Player model, so in each game the player will have the same balance. Please reevaluate what the relationship is here.

### Wireframes or mock-ups (10/10)
Your wireframes are good.

### Additional Information

---
#### Total score (28/30)
---
Graded by: <Sandy Jiang> (sandraj@andrew.cmu.edu)

To view this file with formatting, visit the following page: https://github.com/CMU-Web-Application-Development/Team308/blob/master/feedback/specification-feedback.md
