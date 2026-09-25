Invest your next two days in a small, testable swap-request workflow and organizer feedback. The main uncertainty is whether it improves the existing email process enough to justify another tool.

Your goal is sound: make exchanges easier for volunteers while keeping the organizer responsible for approval. Based on the brief, email is the only established workflow; there is no roster integration or recruited test group. We do not yet know whether the biggest problem is finding a replacement, incomplete requests, slow approvals, or keeping the final roster correct. Those problems call for different solutions.

The concept’s strength is a clear permission boundary: a proposed exchange does not change anyone’s shift until the organizer approves it. Its weakness is that a separate tool can add another inbox and create conflicting versions of the schedule. Without a roster connection, it cannot reliably know availability, eligibility, or whether a shift has already changed.

For the prototype, assume the volunteer has already found someone willing to exchange. Make that limitation explicit. Build one complete path:

- A volunteer enters both people’s shifts and the proposed exchange.
- The other volunteer confirms the details through a demonstration link.
- The organizer sees the original shifts, proposed result, and confirmation, then approves or declines.
- Approval leaves a visible “roster update needed” step until the organizer records that the official schedule has been updated.

Use fictional names and shifts. Show pending, declined, cancelled, and approved states clearly. In two days, a convincing interactive demonstration is feasible; a dependable live service with identity checks, private links, email delivery, and concurrent-request handling is a larger commitment. Do not let a prototype imply that confirmations were sent or a roster was updated when they were not.

Compare this with a cheaper alternative: a standard email template, a single organizer mailbox, and a simple request log. If the main pain is missing information, that may deliver most of the benefit. A web workflow becomes more compelling if repeated confirmation chasing or unclear request status consumes organizer time. A replacement-finding marketplace would require a different experiment and volunteer participation that you do not currently have.

Spend the first part of day one mapping the current process with an organizer, if one is accessible, and reviewing redacted examples they choose to share. Then build the narrow demonstration. On day two, walk the organizer through an ordinary swap, a missing confirmation, and two requests involving the same shift. In parallel, begin recruiting a few volunteers for a later test. If nobody can participate within two days, finish the demo and test script, but treat the audience assumptions as unresolved.

AI can help draft the interface, generate fictional scenarios, and produce prototype code. No runtime AI is needed for the core workflow. The likely cost is your time checking permissions, state transitions, and generated code rather than model usage; a dollar estimate would require your chosen tools and usage. Keep AI out of approval decisions and avoid uploading real volunteer details merely to accelerate development.

The next experiment should compare the prototype with the structured email alternative on the same fictional swap. Observe whether participants can identify who must act next, what they are agreeing to, and whether the official roster has changed. Count clarification requests and organizer actions, and record mistakes. Continue investing in the web tool only if it removes meaningful coordination work without making responsibility or roster status less clear. Organizer feedback can establish operational fit; volunteer usability remains untested until volunteers actually use it.
