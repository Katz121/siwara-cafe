# Map region zoom QA

1. Full responsive suite: all 68 route/viewport checks passed; map region zoom assertion failed on 390px after passing on desktop.
2. Repro: fresh load, full → north → old at 390px returned 100% for each; 1440px returned 100%, 245%, 208%.
3. Hypotheses: width-limited fit formula; resize observer undoing selection; click not delivered. The active button changed correctly and direct source breakpoint reached `zone('north')`, ruling out the missed click. Desktop/mobility differential is consistent with width-limited fitting.
4. Chromium debugger breakpoint at the scale calculation: width=348, height=520, natural image=1358×1938, fit=0.2562592, north bounds=1358×668.61. Width remains the limiting dimension for both full and region modes. This disproves a generic failed-zoom-handler hypothesis.
5. The breakpoint also exposed stale CSS image dimensions 1312×1872 while calculations used 1358×1938. Initialization now sets the image element to its true natural dimensions.
6. Region mode now enforces at least 2× the full-image fit; the overview still fits the whole source image. Panning remains bounded to the actual rendered image. Desktop region fitting retains the larger calculated scale.

Final rerun evidence is recorded in report.json after validation.
