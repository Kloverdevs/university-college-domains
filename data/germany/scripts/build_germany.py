#!/usr/bin/env python3
"""Build the German university and college dataset.
Source: HRK (Hochschulrektorenkonferenz) member institutions.
Germany has ~272 HRK member institutions + Fachhochschulen."""

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent

DE_UNIVERSITIES = [
    # Major research universities (U15/TU9)
    {"name": "RWTH Aachen", "country": "Germany", "state": "North Rhine-Westphalia", "city": "Aachen", "domain": "rwth-aachen.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Freie Universitat Berlin", "country": "Germany", "state": "Berlin", "city": "Berlin", "domain": "fu-berlin.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Humboldt-Universitat zu Berlin", "country": "Germany", "state": "Berlin", "city": "Berlin", "domain": "hu-berlin.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Technische Universitat Berlin", "country": "Germany", "state": "Berlin", "city": "Berlin", "domain": "tu-berlin.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Bonn", "country": "Germany", "state": "North Rhine-Westphalia", "city": "Bonn", "domain": "uni-bonn.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Technische Universitat Braunschweig", "country": "Germany", "state": "Lower Saxony", "city": "Braunschweig", "domain": "tu-braunschweig.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Bremen", "country": "Germany", "state": "Bremen", "city": "Bremen", "domain": "uni-bremen.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Technische Universitat Darmstadt", "country": "Germany", "state": "Hesse", "city": "Darmstadt", "domain": "tu-darmstadt.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Technische Universitat Dresden", "country": "Germany", "state": "Saxony", "city": "Dresden", "domain": "tu-dresden.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Erlangen-Nurnberg", "country": "Germany", "state": "Bavaria", "city": "Erlangen", "domain": "fau.de", "aliases": ["uni-erlangen.de"], "type": "University", "control": "Public"},
    {"name": "Universitat Frankfurt", "country": "Germany", "state": "Hesse", "city": "Frankfurt", "domain": "uni-frankfurt.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Freiburg", "country": "Germany", "state": "Baden-Wurttemberg", "city": "Freiburg", "domain": "uni-freiburg.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Gottingen", "country": "Germany", "state": "Lower Saxony", "city": "Gottingen", "domain": "uni-goettingen.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Hamburg", "country": "Germany", "state": "Hamburg", "city": "Hamburg", "domain": "uni-hamburg.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Leibniz Universitat Hannover", "country": "Germany", "state": "Lower Saxony", "city": "Hannover", "domain": "uni-hannover.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Heidelberg", "country": "Germany", "state": "Baden-Wurttemberg", "city": "Heidelberg", "domain": "uni-heidelberg.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Karlsruher Institut fur Technologie", "country": "Germany", "state": "Baden-Wurttemberg", "city": "Karlsruhe", "domain": "kit.edu", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Koln", "country": "Germany", "state": "North Rhine-Westphalia", "city": "Cologne", "domain": "uni-koeln.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Konstanz", "country": "Germany", "state": "Baden-Wurttemberg", "city": "Konstanz", "domain": "uni-konstanz.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Ludwig-Maximilians-Universitat Munchen", "country": "Germany", "state": "Bavaria", "city": "Munich", "domain": "lmu.de", "aliases": ["uni-muenchen.de"], "type": "University", "control": "Public"},
    {"name": "Technische Universitat Munchen", "country": "Germany", "state": "Bavaria", "city": "Munich", "domain": "tum.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Munster", "country": "Germany", "state": "North Rhine-Westphalia", "city": "Munster", "domain": "uni-muenster.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Stuttgart", "country": "Germany", "state": "Baden-Wurttemberg", "city": "Stuttgart", "domain": "uni-stuttgart.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Tubingen", "country": "Germany", "state": "Baden-Wurttemberg", "city": "Tubingen", "domain": "uni-tuebingen.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Wurzburg", "country": "Germany", "state": "Bavaria", "city": "Wurzburg", "domain": "uni-wuerzburg.de", "aliases": [], "type": "University", "control": "Public"},
    # Other important universities
    {"name": "Universitat Augsburg", "country": "Germany", "state": "Bavaria", "city": "Augsburg", "domain": "uni-augsburg.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Bamberg", "country": "Germany", "state": "Bavaria", "city": "Bamberg", "domain": "uni-bamberg.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Bayreuth", "country": "Germany", "state": "Bavaria", "city": "Bayreuth", "domain": "uni-bayreuth.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Bielefeld", "country": "Germany", "state": "North Rhine-Westphalia", "city": "Bielefeld", "domain": "uni-bielefeld.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Ruhr-Universitat Bochum", "country": "Germany", "state": "North Rhine-Westphalia", "city": "Bochum", "domain": "ruhr-uni-bochum.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Dortmund", "country": "Germany", "state": "North Rhine-Westphalia", "city": "Dortmund", "domain": "tu-dortmund.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Duisburg-Essen", "country": "Germany", "state": "North Rhine-Westphalia", "city": "Duisburg", "domain": "uni-due.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Dusseldorf", "country": "Germany", "state": "North Rhine-Westphalia", "city": "Dusseldorf", "domain": "hhu.de", "aliases": ["uni-duesseldorf.de"], "type": "University", "control": "Public"},
    {"name": "Universitat Greifswald", "country": "Germany", "state": "Mecklenburg-Vorpommern", "city": "Greifswald", "domain": "uni-greifswald.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Halle-Wittenberg", "country": "Germany", "state": "Saxony-Anhalt", "city": "Halle", "domain": "uni-halle.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Technische Universitat Hamburg", "country": "Germany", "state": "Hamburg", "city": "Hamburg", "domain": "tuhh.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Jena", "country": "Germany", "state": "Thuringia", "city": "Jena", "domain": "uni-jena.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Kassel", "country": "Germany", "state": "Hesse", "city": "Kassel", "domain": "uni-kassel.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Kiel", "country": "Germany", "state": "Schleswig-Holstein", "city": "Kiel", "domain": "uni-kiel.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Leipzig", "country": "Germany", "state": "Saxony", "city": "Leipzig", "domain": "uni-leipzig.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Magdeburg", "country": "Germany", "state": "Saxony-Anhalt", "city": "Magdeburg", "domain": "ovgu.de", "aliases": ["uni-magdeburg.de"], "type": "University", "control": "Public"},
    {"name": "Universitat Mainz", "country": "Germany", "state": "Rhineland-Palatinate", "city": "Mainz", "domain": "uni-mainz.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Mannheim", "country": "Germany", "state": "Baden-Wurttemberg", "city": "Mannheim", "domain": "uni-mannheim.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Marburg", "country": "Germany", "state": "Hesse", "city": "Marburg", "domain": "uni-marburg.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Oldenburg", "country": "Germany", "state": "Lower Saxony", "city": "Oldenburg", "domain": "uni-oldenburg.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Osnabruck", "country": "Germany", "state": "Lower Saxony", "city": "Osnabruck", "domain": "uni-osnabrueck.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Paderborn", "country": "Germany", "state": "North Rhine-Westphalia", "city": "Paderborn", "domain": "uni-paderborn.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Passau", "country": "Germany", "state": "Bavaria", "city": "Passau", "domain": "uni-passau.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Potsdam", "country": "Germany", "state": "Brandenburg", "city": "Potsdam", "domain": "uni-potsdam.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Regensburg", "country": "Germany", "state": "Bavaria", "city": "Regensburg", "domain": "uni-regensburg.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Rostock", "country": "Germany", "state": "Mecklenburg-Vorpommern", "city": "Rostock", "domain": "uni-rostock.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat des Saarlandes", "country": "Germany", "state": "Saarland", "city": "Saarbrucken", "domain": "uni-saarland.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Siegen", "country": "Germany", "state": "North Rhine-Westphalia", "city": "Siegen", "domain": "uni-siegen.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Trier", "country": "Germany", "state": "Rhineland-Palatinate", "city": "Trier", "domain": "uni-trier.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Ulm", "country": "Germany", "state": "Baden-Wurttemberg", "city": "Ulm", "domain": "uni-ulm.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Wuppertal", "country": "Germany", "state": "North Rhine-Westphalia", "city": "Wuppertal", "domain": "uni-wuppertal.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Technische Universitat Chemnitz", "country": "Germany", "state": "Saxony", "city": "Chemnitz", "domain": "tu-chemnitz.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Technische Universitat Clausthal", "country": "Germany", "state": "Lower Saxony", "city": "Clausthal-Zellerfeld", "domain": "tu-clausthal.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Technische Universitat Ilmenau", "country": "Germany", "state": "Thuringia", "city": "Ilmenau", "domain": "tu-ilmenau.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Technische Universitat Kaiserslautern", "country": "Germany", "state": "Rhineland-Palatinate", "city": "Kaiserslautern", "domain": "rptu.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Brandenburgische Technische Universitat Cottbus-Senftenberg", "country": "Germany", "state": "Brandenburg", "city": "Cottbus", "domain": "b-tu.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Europa-Universitat Viadrina", "country": "Germany", "state": "Brandenburg", "city": "Frankfurt (Oder)", "domain": "europa-uni.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Erfurt", "country": "Germany", "state": "Thuringia", "city": "Erfurt", "domain": "uni-erfurt.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Weimar", "country": "Germany", "state": "Thuringia", "city": "Weimar", "domain": "uni-weimar.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Hildesheim", "country": "Germany", "state": "Lower Saxony", "city": "Hildesheim", "domain": "uni-hildesheim.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Luneburg", "country": "Germany", "state": "Lower Saxony", "city": "Luneburg", "domain": "leuphana.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Vechta", "country": "Germany", "state": "Lower Saxony", "city": "Vechta", "domain": "uni-vechta.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Flensburg", "country": "Germany", "state": "Schleswig-Holstein", "city": "Flensburg", "domain": "uni-flensburg.de", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Universitat Lubeck", "country": "Germany", "state": "Schleswig-Holstein", "city": "Lubeck", "domain": "uni-luebeck.de", "aliases": [], "type": "University", "control": "Public"},
]

def main():
    de_dir = DATA_DIR / "germany"
    de_dir.mkdir(parents=True, exist_ok=True)
    (de_dir / "scripts").mkdir(exist_ok=True)

    unis = sorted(DE_UNIVERSITIES, key=lambda r: (r["state"], r["name"]))

    with open(de_dir / "universities.json", "w", encoding="utf-8") as f:
        json.dump(unis, f, indent=2, ensure_ascii=False)
    with open(de_dir / "colleges.json", "w", encoding="utf-8") as f:
        json.dump([], f, indent=2, ensure_ascii=False)  # To be expanded with Fachhochschulen

    print(f"Germany Universities: {len(unis)}")

if __name__ == "__main__":
    main()
