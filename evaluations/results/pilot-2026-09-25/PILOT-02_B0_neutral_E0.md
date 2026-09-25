The proposed flow captures the basics of a loan: the item, who borrowed it, and when it is due. That is a useful starting point for keeping track of objects among friends. The main gap is that a loan has no way to end: without a returned state, the list cannot reliably distinguish objects still out from those already back.

Your next investment should be a small, working loan-and-return flow. Give each loan an active or returned state, show active loans by default, and let someone mark an item returned. Keep returned loans in a simple history and allow an accidental return to be undone. Treat “overdue” as an active loan whose due date has passed, so returned items do not continue appearing late.

Start with one screen and save records across reloads. Defer reminders, accounts, and visual polish until the core flow works.

Try it with a few actual household loans. Ask someone to record a loan, identify what is still out, mark an item returned, and correct a mistaken return. Check whether they can complete those tasks without explanation and whether the list remains accurate after reopening it. That gives you concrete evidence for the next improvement.

This assessment is based on the text flow only; without a working application, usability and reliability remain untested.
