# RESET-V30: stronger output pull-ups with original pull-downs

[V29](RESET-V29.md) enlarged both output polarities and failed TT 30 mV delay at 50.5384103494184 ps. Its matched V28 comparison shows Q reaching 50% later by 1.987082135325636 ps, while the Q50-to-OUT50 interval shortens by 1.2043644156613755 ps. All four corners retain correct outputs, completed resets and terminal stress below 1 V. The failed experiment and complete waveform evidence are preserved.

V30 keeps both P8 output pull-ups from V29 and restores only MOPN/MONN to the exact V28 N4 device lines, including all model parameters and terminal parasitics. The other 21 MOS devices and all five MOMs remain identical to V29. Compared with V28, only the two PMOS output devices are enlarged. P8 uses exact zero-warning callback SHA-256 `20855415d9559ad00227138e98d1e759f6c67857f07cd4c5123d67502d0fec87`; the restored N4 parameters also exactly match V28's physical MCKN. No new geometry is fabricated and no physical noise source is disabled.

The experiment tests the output pull-up/pull-down balance before considering reduced input-tail current. Changing the balance can affect loser-output glitches, reset and terminal stress as well as speed. The first private merged-0.8.0 baseline checks TT, SS/low/125 and SF/FS high-voltage cold corners, with all 36 actual decisions and resets, full output validity, every unrounded MOS terminal pair and whole-cycle AVDD energy. Noise and capacitance remain separate required checks; no improvement or qualification is assumed.

Electrical SHA-256: `4e115ae96587505d85011525b8dbe73087c344aa0b867ef39fcc44f7e218f9c4`. The [source](RESET-V30.txt) contains complete RNL checked on a byte-identical mirror. Canonical V27 and every formal record remain unchanged.

![P8 output pull-ups and original N4 pull-downs](reset-v30.png)
