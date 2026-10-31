# BUFFER-V22: stronger CKB pull-up for reset

B21 enlarges only RP/RN MOMs, but its proposed-settings screen fails SS/low/125 reset at 35.42069219051348 ps against 35 ps. All five corners pass 180 actual polarities and completed resets, output validity and full-trace terminal stress. The reset-time failure stops noise expansion. [BUFFER-V21.md](BUFFER-V21.md) preserves the complete failure and measured path.

This experiment retains both 16-finger RP/RN MOMs and changes only MCKP from 4 um/nf4 to 5 um/nf5, with 30 nm length and 1 um finger width fixed. Every other 42 MOS device and all nine MOMs remain electrically identical to B21. The zero-warning callback supplies the geometry and terminal parasitics, SHA-256 `0f9b99701437867b499708c6e500ca31a352b771d4a7a544085f7fc2f609c918`.

The B21 worst reset cycle has CKB at 90% after 14.33700293928296 ps, both RP/RN below 30% after 21.104650816182517 ps, both BP/BN above 90% after 29.37357591729302 ps, and external reset after 35.42069219051348 ps. Stronger CKB pull-up tests an earlier reset assertion through that path. Added clock loading and altered release also affect noise and stress, so no isolated reset or noise benefit is assumed.

The independent private screen uses the merged adc_comp 0.8.0 official testbench baseline without numerical overrides, with APS and actual conservative/gear2only settings checked in the log. It first covers SS hot reset, SF/FS high-voltage cold stress, TT timing and FS/low/125. No formal result or shared testbench, measurement, rule or threshold is modified. Full noise follows only after a useful deterministic pass. Canonical B20 and all earlier failures remain preserved; B22 is not promoted or qualified.

Electrical SHA-256: `379e31cd1bf978f5458ea12c2d011f0273dc918a4db5d1a8ea32b48fad8ee0b3`. The [source](BUFFER-V22.txt) contains complete RNL checked on a byte-identical mirror.

![Comparator with stronger reset clock pull-up](buffer-v22.png)
