# RESET-V4: complementary Q precharge

The DC keeper in V3 prevents small-input decisions. This experiment returns to V2's unheld regenerative core and attacks clock feedthrough with complementary precharge. Each Q node uses a 2 um PMOS gated by CLKC and a 2 um NMOS between AVDD and Q gated by CKB. One N4/P2 inverter generates CKB and a 4.46051 fF MOM device damps that clock node. The tail stays directly clocked. There is no keeper connected to the output.

The hypothesis is that opposite gate transitions reduce net Q-node injection, while the NMOS assists early reset and the PMOS completes the high level. Driver delay, CKB voltage excursions and extra clock-input charge are explicit risks. Existing callback-derived geometries are copied exactly; no new geometry is synthesized and no parasitic is hand scaled.

The independent [RESET-V4.txt](RESET-V4.txt) has 19 MOS and three MOM capacitors. Electrical SHA-256: `f9cf4bb897ed2e9080e83eb7659570310b464618055f8b7c3e8bf79e57e9b3ac`. Full RNL checks with core 0.5.2 on a byte-identical `.scs` mirror: 0 errors, 0 warnings, 0 hints.

![Complementary Q precharge](reset-v4.png)

The first screen retains the same four key corners, current delay stimulus, all-terminal voltage scope, physical output checks and 0.5 ps settings used for V2/V3. This source-freeze commit claims no validation. The canonical baseline is preserved.
