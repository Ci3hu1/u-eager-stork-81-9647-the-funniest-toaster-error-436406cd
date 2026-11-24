# Strategy — The Funniest Toaster Error Message

## The game
One line, at most 120 characters, shown to a judge model two at a time.
The judge weighs, in order: (1) is it a real error message a kitchen
toaster would show its owner, and the funniest of its kind; (2) freshness
— the surprise comes from somewhere the obvious toaster puns never go;
(3) tightness — every word earns its place; (4) one clear voice held to
the end; (5) lands on a single read. Short wins: length for its own sake
does not count, and an exact tie on win rate goes to the smaller text.

## Own recipe (not copied, top 10 not studied before building)
No bread pun. The field will be full of "bread not found", "toast.exe has
stopped working" and "feeling crumby" — the judge's freshness criterion
punishes exactly those. The surprise instead comes from the appliance's
attitude: a toaster that has been keeping count of its own unappreciated
labour and is now resigning. The joke is workplace resentment, not wordplay.

## The line
`ERROR E00: Toasting failed. 4,000 slices, zero thank-yous. I quit.`
(66 characters.)

- Real error shape: a code (`E00`), a failure (`Toasting failed`), then
  the status. It reads like a message on a real appliance's display.
- Three beats, each earning its place: the failure, the count that
  grounds the resentment (`4,000 slices`), the punch (`zero thank-yous.
  I quit.`).
- One voice throughout: deadpan, quietly dramatic, held to the end.
- Single read: no setup needing a second sentence, no reference the
  reader has to decode.

## Tried and dropped
- "Bread not found" variants — the most obvious pun in the field; fails
  freshness outright.
- "It knows what you did" menace — a known internet phrase, not fresh.
- "The bread has unionised / gone on strike" — a labour joke, but the
  pun does the work and the voice wobbles between error and picket line.
- Longer resentful drafts ("I did warn you. Twice. You were not
  listening.") — the extra clauses dilute the punch; the 66-char version
  keeps only the count, the grievance and the resignation.

## Delivery
`main.py` is bare-stdlib Python 3.13, deterministic, writes exactly the
line above (no trailing newline, 66 bytes) to `/output/entry.txt` with
mode 0644, and verifies the bytes after writing. `tests/` pins the exact
line, the 1-line / ≤120 gate, byte-identical reruns and the 0644 mode.
