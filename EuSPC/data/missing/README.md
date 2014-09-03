data/missing
===========

This is the subfolder that contains the missing output of the first and second run of [processEuSPCToAddRxNormAndMeSH.py](https://github.com/OHDSI/KnowledgeBase/blob/d2af5e16c2b6f05d59664b93457f90f90da83dea/EuSPC/processEuSPCToAddRxNormAndMeSH.py) from commit [90f0a68842428c222b9606c05d2d5f129cee7ca4](https://github.com/OHDSI/KnowledgeBase/commit/90f0a68842428c222b9606c05d2d5f129cee7ca4) using the first [getMissingMappings.py](https://github.com/OHDSI/KnowledgeBase/blob/d933222eca84247c7dcbcc03d203141fb3d98198/EuSPC/getMissingMappings.py)


**Files**
- from [getMissingMappings.py](https://github.com/OHDSI/KnowledgeBase/blob/d933222eca84247c7dcbcc03d203141fb3d98198/EuSPC/getMissingMappings.py)
	- format: **drug|substance**
	- [missingMeSHes.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/data/missing/missingMeSHes.txt)
		- single-substance drugs that are only missing the MeSH CUI
	- [missingRxNorms.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/data/missing/missingRxNorms.txt)
		- single substance drugs that are only missing the RxCUI
	- [bothCUIsMissing.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/data/missing/bothCUIsMissing.txt)
		- single-substance drugs that are missing both CUIs
	- [multipleSubstances.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/data/missing/multipleSubstances.txt)
		- all drugs that had multiple substances
- the CUIs that were manually attained through the description below:
	- format: **drug|substance|CUI**
		- [missingMeSHes_CUIs.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/data/missing/missingMeSHes_CUIs.txt)
			- single-substance drugs with their manually found MeSH CUI
		- [missingRxNorms_CUIs.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/data/missing/missingRxNorms_CUIs.txt)
			- single-substance drugs with their manually found RxCUI
	- format: **drug|substance|RxCUI|MeSH**
		- [bothCUIsMissing_CUIs.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/data/missing/bothCUIsMissing_CUIs.txt)
			- single-substance drugs previously missing both CUIs manually searched
		- [multipleSubstances_CUIs.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/data/missing/multipleSubstances_CUIs.txt)
			- all drugs that had multiple substances that hopefully have their CUIs

## Manually Searching RxNorm and MeSH CUIs

I manually added the CUIs missing as shown in the text files above to
the files above *_CUIs.txt using http://bioontology.bioportal.com advanced search
for MeSH and RxNorm where the first run of [processEuSPCToAddRxNormAndMeSH.py](https://github.com/OHDSI/KnowledgeBase/blob/d2af5e16c2b6f05d59664b93457f90f90da83dea/EuSPC/processEuSPCToAddRxNormAndMeSH.py) from commit [90f0a68842428c222b9606c05d2d5f129cee7ca4](https://github.com/OHDSI/KnowledgeBase/commit/90f0a68842428c222b9606c05d2d5f129cee7ca4) using the first [getMissingMappings.py](https://github.com/OHDSI/KnowledgeBase/blob/d933222eca84247c7dcbcc03d203141fb3d98198/EuSPC/getMissingMappings.py)
could not find a match for the substances being searched on.

1. I would search first the drug, then the substance name, and 
2. if all else fails try google.
- For the multipleSubstances_CUIs.txt file, I only searched for the drug name.

#### Still Missing MeSH CUIs:
- Aldurazyme|Laronidase
	- Laronidase is an L molecule for Iduronidase though which has a MeSH CUI
	
- from bothMissingCUIs_CUIs.txt:
	- Ambirix
		- cannot add since it is multiple substances
		- take note that there are many rxnorm results for the type of substance...
	- Advate|Octocog Alfa
	- Atryn|ANTITHROMBIN ALFA
		- This was found in RxNorm form too but the substance and drug are 2 different RxNorms..
	- BeneFIX|NONACOG ALFA
	- Beromun|TASONERMIN
	- Celvapan|A/CALIFORNIA/7/2009 (H1N1)V-LIKE VIRUS
	- ChondroCelect|AUTOLOGOUS HUMAN CARTILAGE CELLS - gives me apoptosis factor though....
	- Helixate NexGen|OCTOCOG ALFA
		- octocog is a very popular ingredient but simply not showing up in MeSH...

- from mulitipleSubstances_CUIs.txt:
	- Infanrix penta
	- M-M-RVaxpro
		- no way to search the MeSH heading for this...
	- ProQuad
	
#### Still Missing RxNorm CUIs:
- IVABRADINE
	- bioportal rxnorm and google give 0 results
- Stiripentol
	- bioportal rxnorm and google give 0 results
- PIXANTRONE
	- bioportal rxnorm and google give 0 results
- PRUCALOPRIDE
	- bioportal rxnorm and google give 0 results
- VINFLUNINE
	- bioportal rxnorm and google give 0 results
- TRABECTEDIN
	- bioportal rxnorm and google give 0 results
	
- from bothMissingCUIs_CUIs.txt
	- Bridion|SUGAMMADEX
	- Brinavess|VERNAKALANT HYDROCHLORIDE
	- Elonva|CORIFOLLITROPIN ALFA
		- seems that I get drotecogin alfa from the substance search
	- Fablyn|LASOFOXIFENE
	- Fampyra|FAMPRIDINE
	- LeukoScan|SULESOMAB
	- Removab|CATUMAXOMAB
	- Ruconest|CONESTAT ALFA
	- Scintimun|BESILESOMAB
	- Thymanax|AGOMELATINE
	- Trobalt|RETIGABINE
	- Valdoxan|AGOMELATINE
	- Vyndaqel|TAFAMIDIS
	- Zutectra|HUMAN HEPATITIS B IMMUNOGLOBULIN
		- unsure what exactly which RxNorm CUI to use...

- from multipleSubstances_CUIs.txt:
	- Azarga
	- DuoTrav
	- Ganfort
	- Kinzalkomb
	- Kivexa
	- Pergoveris
	
#### Still Missing both CUIs:
- Aflunov
	- no RxNorm still and multiple MeSH IDs possible?
- Daronrix|A/VIETNAM/1194/2004 (H5N1)
- Firdapse|AMIFAMPRIDINE
	- I don't see this anywhere in Google or bioportal...
- Foclivia|A/VIETNAM/1194/2004 (H5N1)
	- no straight up results...
- InductOs|DIBOTERMIN ALFA
- Opgenra|EPTOTERMIN ALFA
- Optaflu|INFLUENZA VACCINE SURFACE ANTIGEN INACTIVATED PREPARED IN CELL CULTURES
- Osigraft|EPTOTERMIN ALFA
- Pandemic influenza vaccine H5N1 Baxter|A/VIETNAM/1203/2004 (H5N1)
- Prepandemic influenza vaccine (H5N1) Novartis Vaccines and Diagnostics|A/VIETNAM/1194/2004 (H5N1)
- Prepandrix|A/INDONESIA/05/2005 (H5N1) (PR8-IBCDC-RG2)
- Siklos|HYDROXYCARBAMIDE
- Vedrop|TOCOFERSOLAN
- Vepacel|PRE/PANDEMIC INFLUENZA VACCINE (H5N1)
- Avrodance
- Aerinaze
- CoAprovel
- Competact
- Copalia
- Copalia HCT
- Dafiro
- Dafiro HCT
- Dukoral
- DuoCover
- Efficib
- Eucreas
- Eurartesim
- Evicel
- Fluenz
- Fosavance
- Glubrava
- Icandra
- IDflu
- Ifirmacombi
- Imprida
- Imprida HCT
- Intanza
- IOA (it's a chemical in MeSH)
- Karvezide
- Komboglyze
- Nimenrix
- Onduarp
- Pandemic influenza vaccine (H5N1) (split virion, inactivated, adjuvanted) GlaxoSmithKline Biologicals|PANDEMIC INFLUENZA VACCINE (H5N1) (SPLIT VIRION, INACTIVATED, ADJUVANTED)
	- no way to search this.............
- Pelzont
- Pravafenix
- PritorPlus
- Pumarix
- Rasilamlo
- Rasilez HCT
- Rasitrio
- Riprazo HCT
- Ristfor
- Sprimeo HCT
- Tandemact
- Teysuno
- Tredaptive
- Vantavo
- Velmetia
- Zoely
- Zomarist

##### Notes on medicines with found CUIs (no other comments means usually that it was a direct result):
- Eporatio is apparently [epoetin theta](http://www.ema.europa.eu/ema/index.jsp?curl=pages/medicines/human/medicines/001033/human_med_001204.jsp&mid=WC0b01ac058001d124):
- Fendrix RxCUI just comes from a generic vaccine. This is rDNA though so it might be wrong...
- Flebogamma DIF had an ingredient RxNorm and an injectable product CUI. I chose the injectable product...
- HBVaxPro|HEPATITIS B VACCINE (RDNA) was just given the generic hepatitis B vaccine CUIs
- Helixate NexGen|OCTOCOG ALFA - chose Helixate for rxnorm...
- Kogenate Bayer|OCTOCOG ALFA - used bayer 2000 for the mesh...
- Methylthioninium chloride Proveblue|METHYLTHIONINIUM - used methylene blue for RxNorm
- mixtard is actually insulin, pork - isophane insulin, pork (30:70)... not just INSULIN HUMAN
- Osseor|STRONTIUM RANELATE - chose normal Strontium in RxNorm though there is a pill CUI for it
- Preotact|PARATHYROID HORMONE - used parathyroid hormone...
- Prevenar|PNEUMOCOCCAL POLYSACCHARIDE CONJUGATE VACCINE (ADSORBED) - used the heptavelent conjugate
- Protaphane|INSULIN HUMAN - used the first results of INSULIN HUMAN
- Qutenza|CAPSAICIN - used capsaicin for MeSH
- Silgard is apparently Gardasil according to Wikipedia
- SonoVue|SULFUR HEXAFLUORIDE - used Sulfur in RxNorm (probably wrong...)
- Synflorix|PNEUMOCOCCAL POLYSACCHARIDE CONJUGATE VACCINE (ADSORBED) - used normal pneumococcal vaccine in RxNorm
- Twinrix Adult|HEPATITIS A (INACTIVATED) AND HEPATITIS B (RDNA) VACCINE (ADSORBED) yields many products........
	- only picked the first result even if the 2nd result said "injectable product"
- Evra - used Ortho Evra for both CUIs
- Infanrix penta
	- take note that I just used normal infanrix (probably wrong) in RxNorm
- Irbesartan Hydrochlorothiazide Teva and Zentiva seem to be identical.........
- Levodopa/Carbidopa/Entacapone Orion
	- got the generic version instead of pill version and no Orion in it... in RxNorm
	- seems to be missing the Entacapone in MeSH but used it anyway
- MicardisPlus - based on ingredients, used the Micardis HCT version...
