from sims.run_sensitivity import generate_sensitivity_outputs


def test_generate_sensitivity_outputs(tmp_path):
    df = generate_sensitivity_outputs(
        output_dir=tmp_path,
        policy="sims/configs/policies/baseline.json",
        mrio_config="data/mrio_config.yaml",
        calibration_path="data/calibration.yaml",
        target_scenario="Tariff Shock",
    )
    table_path = tmp_path / "tables" / "world_welfare_sensitivity.tex"
    fig_path = tmp_path / "figs" / "policy_sensitivity.png"
    assert table_path.exists()
    assert fig_path.exists()
    assert {"Run", "FO_pct", "SO_pct"} <= set(df.columns)
    assert len(df) >= 4
