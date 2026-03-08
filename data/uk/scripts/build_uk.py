#!/usr/bin/env python3
"""
Build the UK university and college dataset.
Source: HESA registered providers + curated domain verification.

UK has ~160+ universities and ~200+ further education colleges.
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent

UK_UNIVERSITIES = [
    # Russell Group (24 research-intensive universities)
    {"name": "University of Birmingham", "country": "UK", "state": "England", "city": "Birmingham", "domain": "bham.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Bristol", "country": "UK", "state": "England", "city": "Bristol", "domain": "bristol.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Cambridge", "country": "UK", "state": "England", "city": "Cambridge", "domain": "cam.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Cardiff University", "country": "UK", "state": "Wales", "city": "Cardiff", "domain": "cardiff.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Durham University", "country": "UK", "state": "England", "city": "Durham", "domain": "dur.ac.uk", "aliases": ["durham.ac.uk"], "type": "University", "control": "Public"},
    {"name": "University of Edinburgh", "country": "UK", "state": "Scotland", "city": "Edinburgh", "domain": "ed.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Exeter", "country": "UK", "state": "England", "city": "Exeter", "domain": "exeter.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Glasgow", "country": "UK", "state": "Scotland", "city": "Glasgow", "domain": "gla.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Imperial College London", "country": "UK", "state": "England", "city": "London", "domain": "imperial.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "King's College London", "country": "UK", "state": "England", "city": "London", "domain": "kcl.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Leeds", "country": "UK", "state": "England", "city": "Leeds", "domain": "leeds.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Liverpool", "country": "UK", "state": "England", "city": "Liverpool", "domain": "liverpool.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "London School of Economics", "country": "UK", "state": "England", "city": "London", "domain": "lse.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Manchester", "country": "UK", "state": "England", "city": "Manchester", "domain": "manchester.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Newcastle University", "country": "UK", "state": "England", "city": "Newcastle upon Tyne", "domain": "ncl.ac.uk", "aliases": ["newcastle.ac.uk"], "type": "University", "control": "Public"},
    {"name": "University of Nottingham", "country": "UK", "state": "England", "city": "Nottingham", "domain": "nottingham.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Oxford", "country": "UK", "state": "England", "city": "Oxford", "domain": "ox.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Queen Mary University of London", "country": "UK", "state": "England", "city": "London", "domain": "qmul.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Queen's University Belfast", "country": "UK", "state": "Northern Ireland", "city": "Belfast", "domain": "qub.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Sheffield", "country": "UK", "state": "England", "city": "Sheffield", "domain": "sheffield.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Southampton", "country": "UK", "state": "England", "city": "Southampton", "domain": "soton.ac.uk", "aliases": ["southampton.ac.uk"], "type": "University", "control": "Public"},
    {"name": "University College London", "country": "UK", "state": "England", "city": "London", "domain": "ucl.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Warwick", "country": "UK", "state": "England", "city": "Coventry", "domain": "warwick.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of York", "country": "UK", "state": "England", "city": "York", "domain": "york.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    # Other major English universities
    {"name": "Aston University", "country": "UK", "state": "England", "city": "Birmingham", "domain": "aston.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Bath", "country": "UK", "state": "England", "city": "Bath", "domain": "bath.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Bath Spa University", "country": "UK", "state": "England", "city": "Bath", "domain": "bathspa.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Bedfordshire", "country": "UK", "state": "England", "city": "Luton", "domain": "beds.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Birmingham City University", "country": "UK", "state": "England", "city": "Birmingham", "domain": "bcu.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Bolton", "country": "UK", "state": "England", "city": "Bolton", "domain": "bolton.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Bournemouth University", "country": "UK", "state": "England", "city": "Bournemouth", "domain": "bournemouth.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Bradford", "country": "UK", "state": "England", "city": "Bradford", "domain": "bradford.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Brighton", "country": "UK", "state": "England", "city": "Brighton", "domain": "brighton.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Brunel University London", "country": "UK", "state": "England", "city": "London", "domain": "brunel.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Buckinghamshire New University", "country": "UK", "state": "England", "city": "High Wycombe", "domain": "bucks.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Canterbury Christ Church University", "country": "UK", "state": "England", "city": "Canterbury", "domain": "canterbury.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Central Lancashire", "country": "UK", "state": "England", "city": "Preston", "domain": "uclan.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Chester", "country": "UK", "state": "England", "city": "Chester", "domain": "chester.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Chichester", "country": "UK", "state": "England", "city": "Chichester", "domain": "chi.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "City, University of London", "country": "UK", "state": "England", "city": "London", "domain": "city.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Coventry University", "country": "UK", "state": "England", "city": "Coventry", "domain": "coventry.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Cranfield University", "country": "UK", "state": "England", "city": "Cranfield", "domain": "cranfield.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Cumbria", "country": "UK", "state": "England", "city": "Carlisle", "domain": "cumbria.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "De Montfort University", "country": "UK", "state": "England", "city": "Leicester", "domain": "dmu.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Derby", "country": "UK", "state": "England", "city": "Derby", "domain": "derby.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of East Anglia", "country": "UK", "state": "England", "city": "Norwich", "domain": "uea.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of East London", "country": "UK", "state": "England", "city": "London", "domain": "uel.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Edge Hill University", "country": "UK", "state": "England", "city": "Ormskirk", "domain": "edgehill.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Essex", "country": "UK", "state": "England", "city": "Colchester", "domain": "essex.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Falmouth University", "country": "UK", "state": "England", "city": "Falmouth", "domain": "falmouth.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Gloucestershire", "country": "UK", "state": "England", "city": "Cheltenham", "domain": "glos.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Goldsmiths, University of London", "country": "UK", "state": "England", "city": "London", "domain": "gold.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Greenwich", "country": "UK", "state": "England", "city": "London", "domain": "gre.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Hertfordshire", "country": "UK", "state": "England", "city": "Hatfield", "domain": "herts.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Huddersfield", "country": "UK", "state": "England", "city": "Huddersfield", "domain": "hud.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Hull", "country": "UK", "state": "England", "city": "Hull", "domain": "hull.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Keele University", "country": "UK", "state": "England", "city": "Keele", "domain": "keele.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Kent", "country": "UK", "state": "England", "city": "Canterbury", "domain": "kent.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Kingston University", "country": "UK", "state": "England", "city": "London", "domain": "kingston.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Lancaster University", "country": "UK", "state": "England", "city": "Lancaster", "domain": "lancaster.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Leicester", "country": "UK", "state": "England", "city": "Leicester", "domain": "le.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Lincoln", "country": "UK", "state": "England", "city": "Lincoln", "domain": "lincoln.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Liverpool Hope University", "country": "UK", "state": "England", "city": "Liverpool", "domain": "hope.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Liverpool John Moores University", "country": "UK", "state": "England", "city": "Liverpool", "domain": "ljmu.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of London", "country": "UK", "state": "England", "city": "London", "domain": "london.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "London Metropolitan University", "country": "UK", "state": "England", "city": "London", "domain": "londonmet.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "London South Bank University", "country": "UK", "state": "England", "city": "London", "domain": "lsbu.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Loughborough University", "country": "UK", "state": "England", "city": "Loughborough", "domain": "lboro.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Manchester", "country": "UK", "state": "England", "city": "Manchester", "domain": "manchester.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Manchester Metropolitan University", "country": "UK", "state": "England", "city": "Manchester", "domain": "mmu.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Middlesex University", "country": "UK", "state": "England", "city": "London", "domain": "mdx.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Northampton", "country": "UK", "state": "England", "city": "Northampton", "domain": "northampton.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Northumbria University", "country": "UK", "state": "England", "city": "Newcastle upon Tyne", "domain": "northumbria.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Norwich University of the Arts", "country": "UK", "state": "England", "city": "Norwich", "domain": "nua.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Nottingham Trent University", "country": "UK", "state": "England", "city": "Nottingham", "domain": "ntu.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Open University", "country": "UK", "state": "England", "city": "Milton Keynes", "domain": "open.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Oxford Brookes University", "country": "UK", "state": "England", "city": "Oxford", "domain": "brookes.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Plymouth", "country": "UK", "state": "England", "city": "Plymouth", "domain": "plymouth.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Portsmouth", "country": "UK", "state": "England", "city": "Portsmouth", "domain": "port.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Reading", "country": "UK", "state": "England", "city": "Reading", "domain": "reading.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Roehampton University", "country": "UK", "state": "England", "city": "London", "domain": "roehampton.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Royal Holloway, University of London", "country": "UK", "state": "England", "city": "Egham", "domain": "royalholloway.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Salford", "country": "UK", "state": "England", "city": "Salford", "domain": "salford.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Sheffield Hallam University", "country": "UK", "state": "England", "city": "Sheffield", "domain": "shu.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "SOAS, University of London", "country": "UK", "state": "England", "city": "London", "domain": "soas.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Solent University", "country": "UK", "state": "England", "city": "Southampton", "domain": "solent.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Staffordshire University", "country": "UK", "state": "England", "city": "Stoke-on-Trent", "domain": "staffs.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Sunderland", "country": "UK", "state": "England", "city": "Sunderland", "domain": "sunderland.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Surrey", "country": "UK", "state": "England", "city": "Guildford", "domain": "surrey.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Sussex", "country": "UK", "state": "England", "city": "Brighton", "domain": "sussex.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Swansea University", "country": "UK", "state": "Wales", "city": "Swansea", "domain": "swansea.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Teesside University", "country": "UK", "state": "England", "city": "Middlesbrough", "domain": "tees.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of the Arts London", "country": "UK", "state": "England", "city": "London", "domain": "arts.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of the West of England", "country": "UK", "state": "England", "city": "Bristol", "domain": "uwe.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of West London", "country": "UK", "state": "England", "city": "London", "domain": "uwl.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Westminster", "country": "UK", "state": "England", "city": "London", "domain": "westminster.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Winchester", "country": "UK", "state": "England", "city": "Winchester", "domain": "winchester.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Wolverhampton", "country": "UK", "state": "England", "city": "Wolverhampton", "domain": "wlv.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Worcester", "country": "UK", "state": "England", "city": "Worcester", "domain": "worc.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    # Scotland
    {"name": "University of Aberdeen", "country": "UK", "state": "Scotland", "city": "Aberdeen", "domain": "abdn.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Abertay University", "country": "UK", "state": "Scotland", "city": "Dundee", "domain": "abertay.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Dundee", "country": "UK", "state": "Scotland", "city": "Dundee", "domain": "dundee.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Edinburgh Napier University", "country": "UK", "state": "Scotland", "city": "Edinburgh", "domain": "napier.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Glasgow Caledonian University", "country": "UK", "state": "Scotland", "city": "Glasgow", "domain": "gcu.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Heriot-Watt University", "country": "UK", "state": "Scotland", "city": "Edinburgh", "domain": "hw.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Robert Gordon University", "country": "UK", "state": "Scotland", "city": "Aberdeen", "domain": "rgu.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of St Andrews", "country": "UK", "state": "Scotland", "city": "St Andrews", "domain": "st-andrews.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Stirling", "country": "UK", "state": "Scotland", "city": "Stirling", "domain": "stir.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Strathclyde", "country": "UK", "state": "Scotland", "city": "Glasgow", "domain": "strath.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of the West of Scotland", "country": "UK", "state": "Scotland", "city": "Paisley", "domain": "uws.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of the Highlands and Islands", "country": "UK", "state": "Scotland", "city": "Inverness", "domain": "uhi.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Queen Margaret University", "country": "UK", "state": "Scotland", "city": "Edinburgh", "domain": "qmu.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    # Wales
    {"name": "Aberystwyth University", "country": "UK", "state": "Wales", "city": "Aberystwyth", "domain": "aber.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Bangor University", "country": "UK", "state": "Wales", "city": "Bangor", "domain": "bangor.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of South Wales", "country": "UK", "state": "Wales", "city": "Pontypridd", "domain": "southwales.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Wrexham University", "country": "UK", "state": "Wales", "city": "Wrexham", "domain": "wrexham.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    # Northern Ireland
    {"name": "Ulster University", "country": "UK", "state": "Northern Ireland", "city": "Belfast", "domain": "ulster.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    # Specialist / Private
    {"name": "University of Buckingham", "country": "UK", "state": "England", "city": "Buckingham", "domain": "buckingham.ac.uk", "aliases": [], "type": "University", "control": "Private"},
    {"name": "BPP University", "country": "UK", "state": "England", "city": "London", "domain": "bpp.com", "aliases": [], "type": "University", "control": "Private"},
    {"name": "University of Law", "country": "UK", "state": "England", "city": "London", "domain": "law.ac.uk", "aliases": [], "type": "University", "control": "Private"},
    {"name": "Regent's University London", "country": "UK", "state": "England", "city": "London", "domain": "regents.ac.uk", "aliases": [], "type": "University", "control": "Private"},
    {"name": "Royal Academy of Music", "country": "UK", "state": "England", "city": "London", "domain": "ram.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Royal College of Art", "country": "UK", "state": "England", "city": "London", "domain": "rca.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Royal College of Music", "country": "UK", "state": "England", "city": "London", "domain": "rcm.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Royal Northern College of Music", "country": "UK", "state": "England", "city": "Manchester", "domain": "rncm.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Guildhall School of Music and Drama", "country": "UK", "state": "England", "city": "London", "domain": "gsmd.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Royal Conservatoire of Scotland", "country": "UK", "state": "Scotland", "city": "Glasgow", "domain": "rcs.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Royal Welsh College of Music and Drama", "country": "UK", "state": "Wales", "city": "Cardiff", "domain": "rwcmd.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University for the Creative Arts", "country": "UK", "state": "England", "city": "Farnham", "domain": "uca.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Arts University Bournemouth", "country": "UK", "state": "England", "city": "Bournemouth", "domain": "aub.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Leeds Arts University", "country": "UK", "state": "England", "city": "Leeds", "domain": "leedsarts.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Ravensbourne University London", "country": "UK", "state": "England", "city": "London", "domain": "ravensbourne.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Rose Bruford College", "country": "UK", "state": "England", "city": "London", "domain": "bruford.ac.uk", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Trinity Laban Conservatoire", "country": "UK", "state": "England", "city": "London", "domain": "trinitylaban.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Suffolk", "country": "UK", "state": "England", "city": "Ipswich", "domain": "uos.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Leeds Beckett University", "country": "UK", "state": "England", "city": "Leeds", "domain": "leedsbeckett.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Leeds Trinity University", "country": "UK", "state": "England", "city": "Leeds", "domain": "leedstrinity.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "St Mary's University, Twickenham", "country": "UK", "state": "England", "city": "London", "domain": "stmarys.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Newman University", "country": "UK", "state": "England", "city": "Birmingham", "domain": "newman.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "York St John University", "country": "UK", "state": "England", "city": "York", "domain": "yorksj.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Bishop Grosseteste University", "country": "UK", "state": "England", "city": "Lincoln", "domain": "bishopg.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Anglia Ruskin University", "country": "UK", "state": "England", "city": "Cambridge", "domain": "aru.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "University of Sunderland", "country": "UK", "state": "England", "city": "Sunderland", "domain": "sunderland.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Harper Adams University", "country": "UK", "state": "England", "city": "Newport", "domain": "harper-adams.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Royal Agricultural University", "country": "UK", "state": "England", "city": "Cirencester", "domain": "rau.ac.uk", "aliases": [], "type": "University", "control": "Public"},
    {"name": "Writtle University College", "country": "UK", "state": "England", "city": "Chelmsford", "domain": "writtle.ac.uk", "aliases": [], "type": "College", "control": "Public"},
    {"name": "London Business School", "country": "UK", "state": "England", "city": "London", "domain": "london.edu", "aliases": [], "type": "University", "control": "Public"},
]

UK_COLLEGES = [
    {"name": "Imperial College Business School", "country": "UK", "state": "England", "city": "London", "domain": "imperial.ac.uk", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Birkbeck, University of London", "country": "UK", "state": "England", "city": "London", "domain": "bbk.ac.uk", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Courtauld Institute of Art", "country": "UK", "state": "England", "city": "London", "domain": "courtauld.ac.uk", "aliases": [], "type": "Institute", "control": "Public"},
    {"name": "London School of Hygiene and Tropical Medicine", "country": "UK", "state": "England", "city": "London", "domain": "lshtm.ac.uk", "aliases": [], "type": "Institute", "control": "Public"},
    {"name": "Institute of Cancer Research", "country": "UK", "state": "England", "city": "London", "domain": "icr.ac.uk", "aliases": [], "type": "Institute", "control": "Public"},
    {"name": "Hartpury University and Hartpury College", "country": "UK", "state": "England", "city": "Gloucester", "domain": "hartpury.ac.uk", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Conservatoire for Dance and Drama", "country": "UK", "state": "England", "city": "London", "domain": "cdd.ac.uk", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Northern School of Contemporary Dance", "country": "UK", "state": "England", "city": "Leeds", "domain": "nscd.ac.uk", "aliases": [], "type": "College", "control": "Public"},
    {"name": "Liverpool Institute for Performing Arts", "country": "UK", "state": "England", "city": "Liverpool", "domain": "lipa.ac.uk", "aliases": [], "type": "Institute", "control": "Private"},
    {"name": "SAE Institute", "country": "UK", "state": "England", "city": "London", "domain": "sae.edu", "aliases": [], "type": "Institute", "control": "Private"},
]


def main():
    # Split and save
    from pathlib import Path
    uk_dir = DATA_DIR / "uk"
    uk_dir.mkdir(parents=True, exist_ok=True)
    (uk_dir / "scripts").mkdir(exist_ok=True)

    unis = sorted(UK_UNIVERSITIES, key=lambda r: (r["state"], r["name"]))
    cols = sorted(UK_COLLEGES, key=lambda r: (r["state"], r["name"]))

    # Dedup
    seen = set()
    deduped_unis = []
    for u in unis:
        if u["name"] not in seen:
            seen.add(u["name"])
            deduped_unis.append(u)

    with open(uk_dir / "universities.json", "w", encoding="utf-8") as f:
        json.dump(deduped_unis, f, indent=2, ensure_ascii=False)
    with open(uk_dir / "colleges.json", "w", encoding="utf-8") as f:
        json.dump(cols, f, indent=2, ensure_ascii=False)

    print(f"UK Universities: {len(deduped_unis)}")
    print(f"UK Colleges: {len(cols)}")
    print(f"UK Total: {len(deduped_unis) + len(cols)}")


if __name__ == "__main__":
    main()
