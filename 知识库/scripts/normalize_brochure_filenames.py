from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BROCHURE_DIR = ROOT / "单页"


RENAME_MAP = {
    "单页/FL3000/CN(Simplified)_20251110_FJD FL3000_Brochure.pdf": "单页/FL3000/CN(Simplified)_20251110_FJD FL3000 Brochure.pdf",
    "单页/FL3000/CN(simplified)_20251110_FJD FL3000_Brochure (for print).pdf": "单页/FL3000/CN(Simplified)_20251110_FJD FL3000 Brochure(for print).pdf",
    "单页/FL3000/EN_20251118_FJD FL3000_Brochure.pdf": "单页/FL3000/EN_20251118_FJD FL3000 Brochure.pdf",
    "单页/FL3000/EN_20251120_FJD FL3000_Brochure (for print).pdf": "单页/FL3000/EN_20251120_FJD FL3000 Brochure(for print).pdf",
    "单页/FL3000/ES_20251103_FJD FL3000 Brochure (print).pdf": "单页/FL3000/ES_20251103_FJD FL3000 Brochure(for print).pdf",
    "单页/FL3000/FR_20260122_FJD FL3000_Brochure (for print).pdf": "单页/FL3000/FR_20260122_FJD FL3000 Brochure(for print).pdf",
    "单页/FL3000/FR_20260122_FJD FL3000_Brochure.pdf": "单页/FL3000/FR_20260122_FJD FL3000 Brochure.pdf",
    "单页/FL3000/ISL_20251107_FJD FL3000 Brochure (for print).pdf": "单页/FL3000/ISL_20251107_FJD FL3000 Brochure(for print).pdf",
    "单页/FL3000/ISL_20251107_FJD FL3000 Brochure .pdf": "单页/FL3000/ISL_20251107_FJD FL3000 Brochure.pdf",
    "单页/FL3000/IT_20250909_FJD FL3000 Brochure (for print).pdf": "单页/FL3000/IT_20250909_FJD FL3000 Brochure(for print).pdf",
    "单页/FL3000/JP_20250912_FJD FL3000 Brochure (for print).pdf": "单页/FL3000/JP_20250912_FJD FL3000 Brochure(for print).pdf",
    "单页/FL3000/PL_FL3000_20260225 Brochure (for print).pdf": "单页/FL3000/PL_20260225_FJD FL3000 Brochure(for print).pdf",
    "单页/FL3000/PL_FL3000_20260225 Brochure.pdf": "单页/FL3000/PL_20260225_FJD FL3000 Brochure.pdf",
    "单页/FR4000/CN(Simplified)_20251101_FJD FR4000.pdf": "单页/FR4000/CN(Simplified)_20251101_FJD FR4000 Brochure.pdf",
    "单页/FR4000/CN(Traditional)_20251103_FJD FR4000.pdf": "单页/FR4000/CN(Traditional)_20251103_FJD FR4000 Brochure.pdf",
    "单页/FR4000/DE_20251101_FJD FR4000_Brochure (for print).pdf": "单页/FR4000/DE_20251101_FJD FR4000 Brochure(for print).pdf",
    "单页/FR4000/DE_20251101_FJD FR4000_Brochure.pdf": "单页/FR4000/DE_20251101_FJD FR4000 Brochure.pdf",
    "单页/FR4000/EN_20251118_FJD FR4000_Brochure (for print ).pdf": "单页/FR4000/EN_20251118_FJD FR4000 Brochure(for print).pdf",
    "单页/FR4000/EN_20251121_FJD FR4000_Brochure.pdf": "单页/FR4000/EN_20251121_FJD FR4000 Brochure.pdf",
    "单页/FR4000/ES_20260106_FJD FR4000_ Brochure.pdf": "单页/FR4000/ES_20260106_FJD FR4000 Brochure.pdf",
    "单页/FR4000/FR_20251107_FJD FR4000 .pdf": "单页/FR4000/FR_20251107_FJD FR4000 Brochure(for print).pdf",
    "单页/FR4000/FR_20251107_FJD FR4000.pdf": "单页/FR4000/FR_20251107_FJD FR4000 Brochure.pdf",
    "单页/FR4000/IT_20260108_FJD FR4000_Brochure (Print).pdf": "单页/FR4000/IT_20260108_FJD FR4000 Brochure(for print).pdf",
    "单页/FR4000/IT_20260108_FJD FR4000_Brochure.pdf": "单页/FR4000/IT_20260108_FJD FR4000 Brochure.pdf",
    "单页/FR4000/JP_20251101_FJD FR4000 _Brochure.pdf": "单页/FR4000/JP_20251101_FJD FR4000 Brochure.pdf",
    "单页/FR4000/JP_20251101_FJD FR4000_brochure (print)pdf.pdf": "单页/FR4000/JP_20251101_FJD FR4000 Brochure(for print).pdf",
    "单页/FRX/(打印 CMYK 有出血)ES_20260119_FJD FRX _FINAL.pdf": "单页/FRX/ES_20260119_FJD FRX Brochure(for print).pdf",
    "单页/FRX/(打印 CMYK 有出血)FR_20260119_FJD FRX _FINAL.pdf": "单页/FRX/FR_20260119_FJD FRX Brochure(for print).pdf",
    "单页/FRX/(线上 RGB 没有出血)ES_20260119_FJD FRX _FINAL.pdf": "单页/FRX/ES_20260119_FJD FRX Brochure.pdf",
    "单页/FRX/(线上 RGB 没有出血)FR_20260119_FJD FRX _FINAL.pdf": "单页/FRX/FR_20260119_FJD FRX Brochure.pdf",
    "单页/FRX/CN_20251118_FJD FRX_Brochure.pdf": "单页/FRX/CN(Simplified)_20251118_FJD FRX Brochure.pdf",
    "单页/FRX/DE_20251120_FJD FRX_Brochure (for print).pdf": "单页/FRX/DE_20251120_FJD FRX Brochure(for print).pdf",
    "单页/FRX/DE_20251120_FJD FRX_Brochure.pdf": "单页/FRX/DE_20251120_FJD FRX Brochure.pdf",
    "单页/FRX/EN_20251119_FJD FRX_Brochure.pdf": "单页/FRX/EN_20251119_FJD FRX Brochure.pdf",
    "单页/FRX/EN_20251120_FJD FRX_Brochure (for print).pdf": "单页/FRX/EN_20251120_FJD FRX Brochure(for print).pdf",
    "单页/FRX/IT_20260106_FJD FRX_Brochure (print).pdf": "单页/FRX/IT_20260106_FJD FRX Brochure(for print).pdf",
    "单页/FRX/IT_20260106_FJD FRX_Brochure.pdf": "单页/FRX/IT_20260106_FJD FRX Brochure.pdf",
    "单页/FRX/JP_20251209_FJD FRX_Brochure.pdf": "单页/FRX/JP_20251209_FJD FRX Brochure.pdf",
    "单页/FRX/（打印版）JP_20251026_FJD FRX.pdf .pdf": "单页/FRX/JP_20251026_FJD FRX Brochure(for print).pdf",
    "单页/FV2000/EN_20251118_FJD FV2000_Brochure.pdf": "单页/FV2000/EN_20251118_FJD FV2000 Brochure.pdf",
    "单页/FV2000/EN_20251120_FJD FV2000_Brochure (for print).pdf": "单页/FV2000/EN_20251120_FJD FV2000 Brochure(for print).pdf",
    "单页/FV2000/IT_20260108_FJD FV2000_BROCHURE (Print).pdf": "单页/FV2000/IT_20260108_FJD FV2000 Brochure(for print).pdf",
    "单页/FV2000/IT_20260108_FJD FV2000_BROCHURE final.pdf": "单页/FV2000/IT_20260108_FJD FV2000 Brochure.pdf",
    "单页/RCM01/DE_20260205_FJD RCM01_Brochure.pdf .pdf": "单页/RCM01/DE_20260205_FJD RCM01 Brochure.pdf",
    "单页/RCM01/DE_20260206_FJD RCM01_Brochure (for print).pdf": "单页/RCM01/DE_20260206_FJD RCM01 Brochure(for print).pdf",
    "单页/RCM01/EN_20260205_FJD RCM01_Brochure (for print).pdf": "单页/RCM01/EN_20260205_FJD RCM01 Brochure(for print).pdf",
    "单页/RCM01/EN_20260205_FJD RCM01_Brochure.pdf": "单页/RCM01/EN_20260205_FJD RCM01 Brochure.pdf",
    "单页/RCM01/FR_20260127_FJD RCM01_Brochure.pdf": "单页/RCM01/FR_20260127_FJD RCM01 Brochure.pdf",
    "单页/RCM01/IT_20260126_FJD RCM01_Brochure.pdf": "单页/RCM01/IT_20260126_FJD RCM01 Brochure.pdf",
    "单页/RCM01/JP_20260108_FJD RCM01_Brochure.pdf": "单页/RCM01/JP_20260108_FJD RCM01 Brochure.pdf",
    "单页/RCM01/打印版CN(Simplified)_20260109_FJD RCM01_Brochure (1).pdf": "单页/RCM01/CN(Simplified)_20260109_FJD RCM01 Brochure(for print).pdf",
    "单页/RCM01/打印版CN(Traditional)_20260108_FJD RCM01_Brochure (1).pdf": "单页/RCM01/CN(Traditional)_20260108_FJD RCM01 Brochure(for print).pdf",
    "单页/RCM01/简中_20260108_FJD RCM01_单页.pdf": "单页/RCM01/CN(Simplified)_20260108_FJD RCM01 Brochure.pdf",
    "单页/RCM01/繁中_20260108_FJD RCM01_单页.pdf": "单页/RCM01/CN(Traditional)_20260108_FJD RCM01 Brochure.pdf",
    "单页/RCM01/（打印版）FR_20260127_FJD RCM01_Brochure终稿.pdf 副本.pdf": "单页/RCM01/FR_20260127_FJD RCM01 Brochure(for print).pdf",
    "单页/RCM01/（打印版）IT_20260126_FJD RCM01_Brochure终稿.pdf.pdf": "单页/RCM01/IT_20260126_FJD RCM01 Brochure(for print).pdf",
    "单页/RCM01/（打印版）JA _20260203_FJD_RCM01_Brochure.pdf.pdf": "单页/RCM01/JP_20260203_FJD RCM01 Brochure(for print).pdf",
    "单页/RM21 combo/(打印 CMYK 有出血)FR_20260123_FJD_RM21 COMBO-BROCHUR_5稿.pdf": "单页/RM21 combo/FR_20260123_FJD RM21 Combo Brochure(for print).pdf",
    "单页/RM21 combo/CN(Simplified)_20260120_FJD_RM21 combo-brochure.pdf": "单页/RM21 combo/CN(Simplified)_20260120_FJD RM21 Combo Brochure.pdf",
    "单页/RM21 combo/CN(Traditional)_20260130_FJD_RM21 combo-Brochure.pdf": "单页/RM21 combo/CN(Traditional)_20260130_FJD RM21 Combo Brochure.pdf",
    "单页/RM21 combo/CN（繁中）_20260120_FJD_RM21 combo-brochure.pdf .pdf": "单页/RM21 combo/CN(Traditional)_20260120_FJD RM21 Combo Brochure(for print).pdf",
    "单页/RM21 combo/DE_20260123_FJD_RM21 Combo_Brochure (for print).pdf": "单页/RM21 combo/DE_20260123_FJD RM21 Combo Brochure(for print).pdf",
    "单页/RM21 combo/DE_20260123_FJD_RM21 Combo_Brochure.pdf": "单页/RM21 combo/DE_20260123_FJD RM21 Combo Brochure.pdf",
    "单页/RM21 combo/EN_20251215_FJD_RM21 Combo_Brochure (for print).pdf": "单页/RM21 combo/EN_20251215_FJD RM21 Combo Brochure(for print).pdf",
    "单页/RM21 combo/EN_20260303_FJD_RM21 Combo_Brochure.pdf": "单页/RM21 combo/EN_20260303_FJD RM21 Combo Brochure.pdf",
    "单页/RM21 combo/ES_20260107_FJD_RM21 combo-brochure.pdf": "单页/RM21 combo/ES_20260107_FJD RM21 Combo Brochure.pdf",
    "单页/RM21 combo/ES_20260107_FJD_RM21 combo-brochure（print）.pdf": "单页/RM21 combo/ES_20260107_FJD RM21 Combo Brochure(for print).pdf",
    "单页/RM21 combo/FR_20260120_FJD_RM21 combo-Brochure.pdf": "单页/RM21 combo/FR_20260120_FJD RM21 Combo Brochure.pdf",
    "单页/RM21 combo/IT_20260108_FJD_RM21 combo-Brochure (Print).pdf": "单页/RM21 combo/IT_20260108_FJD RM21 Combo Brochure(for print).pdf",
    "单页/RM21 combo/IT_20260108_FJD_RM21 combo-brochure.pdf": "单页/RM21 combo/IT_20260108_FJD RM21 Combo Brochure.pdf",
    "单页/RM21 combo/打印版CN简中_20260120_FJD_RM21 combo-brochure.pdf .pdf": "单页/RM21 combo/CN(Simplified)_20260120_FJD RM21 Combo Brochure(for print).pdf",
    "单页/Titan/EN_20260227_FJD Titan_Brochure.pdf": "单页/Titan/EN_20260227_FJD Titan Brochure.pdf",
    "单页/Titan/EN_20260304_FJD Titan_Brochure (for print).pdf": "单页/Titan/EN_20260304_FJD Titan Brochure(for print).pdf",
}


CANONICAL_PATTERN = re.compile(
    r"^(?:CN\(Simplified\)|CN\(Traditional\)|DE|EN|ES|FR|ISL|IT|JP|PL)_\d{8}_FJD .+ Brochure(?:\(for print\))?\.pdf$"
)


def rename_files() -> list[tuple[Path, Path]]:
    renamed: list[tuple[Path, Path]] = []
    temp_moves: list[tuple[Path, Path]] = []
    final_moves: list[tuple[Path, Path]] = []

    for source_rel, target_rel in RENAME_MAP.items():
        source = ROOT / source_rel
        target = ROOT / target_rel
        if not source.exists():
            continue
        if source == target:
            continue
        if target.exists() and target != source:
            raise FileExistsError(f"Target already exists: {target}")
        temp = source.with_name(source.name + ".rename_tmp")
        if temp.exists():
            raise FileExistsError(f"Temporary path already exists: {temp}")
        temp_moves.append((source, temp))
        final_moves.append((temp, target))
        renamed.append((source, target))

    for source, temp in temp_moves:
        source.rename(temp)

    for temp, target in final_moves:
        target.parent.mkdir(parents=True, exist_ok=True)
        temp.rename(target)

    return renamed


def find_nonconforming_pdfs() -> list[Path]:
    invalid: list[Path] = []
    for path in sorted(BROCHURE_DIR.rglob("*.pdf")):
        if path.name.startswith("."):
            continue
        if not CANONICAL_PATTERN.match(path.name):
            invalid.append(path)
    return invalid


def main() -> None:
    renamed = rename_files()
    invalid = find_nonconforming_pdfs()

    print(f"Renamed {len(renamed)} files.")
    for source, target in renamed:
        print(f"- {source.relative_to(ROOT)} -> {target.relative_to(ROOT)}")

    if invalid:
        print("\nFiles still not matching canonical format:")
        for path in invalid:
            print(f"- {path.relative_to(ROOT)}")
        raise SystemExit(1)

    print("\nAll brochure PDFs now match the canonical naming pattern.")


if __name__ == "__main__":
    main()
