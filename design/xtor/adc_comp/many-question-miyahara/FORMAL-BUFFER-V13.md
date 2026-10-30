# BUFFER-V13: genuine new-source formal gates

The canonical source is electrically identical to the ten-key-corner and tight-convergence source. The existing official runner, original testbench, numerical settings, measurement and recorder are unchanged. Private screens are not adopted as official records.

## TT capacitance and kickback: pass

Run `20261031-070641-13bb-tb_comp_kickback` starts from clean source commit `d4c88fe23e96627826be3e39d56de1ba71ed01ab`. Electrical SHA-256 is `ce5b3787a38ea80eb6775686bbe1df538e8864a2deb3d5f784d67e119b6146e0`.

| Metric | Measured | Limit |
|---|---:|---:|
| Input capacitance | 19.328731218738 fF | 20 fF |
| CLKC capacitance | 9.604337628086 fF | 16 fF |
| Differential kickback | 0.001649260400 uV | 40 uV |

The [official TT result](../../../../results/adc_comp/tb_comp_kickback/xtor-many-question-miyahara/tt_nom_27.json) retains its actual clean-source metadata. The complete original run and result figures are SHA-verified in a private archive, and the exact owned remote directory is confirmed absent. Execution uses +aps without explicit +mt; logs confirm effective single-thread operation.

One of 92 current result files now matches B13; 91 old-source records remain stale. The next gate is the prescribed official TT 17 x 512 noise test, with the original bandwidth and seed. No B12 noise, remaining-corner, Monte Carlo or mixed-top result transfers.
