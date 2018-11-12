import os
from tempfile import NamedTemporaryFile
from pathlib import Path

from click.testing import CliRunner
import pytest

from ncbi_taxid import __version__
import ncbi_taxid.cli

test_data = """BOT1cds1	PKP60081.1	29.0	138	96	2	7	143	8	144	2.5e-07	65.5	209	217	63.1	PKP60081.1 hypothetical protein CVT88_04030 [Candidatus Altiarchaeales archaeon HGW-Altiarchaeales-1]	2013673
BOT1cds1	PJI86295.1	36.6	71	39	3	22	90	175	241	8.7e+00	40.4	295	217	31.8	PJI86295.1 4-diphosphocytidyl-2-C-methyl-D-erythritol kinase [Yoonia maricola]	420999
BOT1cds1	WP_100368596.1	36.6	71	39	3	22	90	165	231	8.7e+00	40.4	285	217	31.8	WP_100368596.1 4-(cytidine 5'-diphospho)-2-C-methyl-D-erythritol kinase [Yoonia maricola]	420999
BOT1cds2	WP_106860599.1	30.7	274	188	1	1	274	1	272	6.2e-35	157.5	273	275	99.6	WP_106860599.1 hypothetical protein [Candidatus Sulfopaludibacter sp. SbA4]	2043165
BOT1cds2	SPE37964.1	36.3	190	120	1	86	275	1	189	4.4e-25	124.8	192	275	69.1	SPE37964.1 hypothetical protein SBA6_80035 [Candidatus Sulfopaludibacter sp. SbA6]	2043166
BOT1cds2	WP_105313039.1	36.2	177	112	1	99	275	1	176	2.7e-22	115.5	179	275	64.4	WP_105313039.1 hypothetical protein [Candidatus Sulfopaludibacter sp. SbA6]	2043166
BOT1cds2	WP_048155622.1	28.2	280	187	7	3	275	6	278	4.6e-22	114.8	279	275	99.3	WP_048155622.1 MULTISPECIES: hypothetical protein [Methanosarcina]	2207;1434108;1860098
BOT1cds2	PKP60082.1	28.0	264	172	8	24	275	4	261	3.1e-18	102.1	266	275	91.6	PKP60082.1 hypothetical protein CVT88_04035 [Candidatus Altiarchaeales archaeon HGW-Altiarchaeales-1]	2013673
BOT1cds2	POZ52851.1	25.6	270	178	8	1	258	10	268	4.9e-08	68.2	295	275	93.8	POZ52851.1 hypothetical protein AADEFJLK_01460 [Methylovulum psychrotolerans]	1704499
BOT1cds2	WP_103973803.1	25.6	270	178	8	1	258	1	259	4.9e-08	68.2	286	275	93.8	WP_103973803.1 hypothetical protein [Methylovulum psychrotolerans]	1704499
"""

test_expected_result = """BOT1cds1	PKP60081.1	29.0	138	96	2	7	143	8	144	2.5e-07	65.5	209	217	63.1	PKP60081.1 hypothetical protein CVT88_04030 [Candidatus Altiarchaeales archaeon HGW-Altiarchaeales-1]	2013673	Archaea	Euryarchaeota	UNKNOWN	Candidatus Altiarchaeales	UNKNOWN	UNKNOWN	Candidatus Altiarchaeales archaeon HGW-Altiarchaeales-1
BOT1cds1	PJI86295.1	36.6	71	39	3	22	90	175	241	8.7e+00	40.4	295	217	31.8	PJI86295.1 4-diphosphocytidyl-2-C-methyl-D-erythritol kinase [Yoonia maricola]	420999	Bacteria	Proteobacteria	Alphaproteobacteria	Rhodobacterales	Rhodobacteraceae	Yoonia	Yoonia maricola
BOT1cds1	WP_100368596.1	36.6	71	39	3	22	90	165	231	8.7e+00	40.4	285	217	31.8	WP_100368596.1 4-(cytidine 5'-diphospho)-2-C-methyl-D-erythritol kinase [Yoonia maricola]	420999	Bacteria	Proteobacteria	Alphaproteobacteria	Rhodobacterales	Rhodobacteraceae	Yoonia	Yoonia maricola
BOT1cds2	WP_106860599.1	30.7	274	188	1	1	274	1	272	6.2e-35	157.5	273	275	99.6	WP_106860599.1 hypothetical protein [Candidatus Sulfopaludibacter sp. SbA4]	2043165	Bacteria	Acidobacteria	Solibacteres	Solibacterales	Solibacteraceae	Candidatus Sulfopaludibacter	Candidatus Sulfopaludibacter sp. SbA4
BOT1cds2	SPE37964.1	36.3	190	120	1	86	275	1	189	4.4e-25	124.8	192	275	69.1	SPE37964.1 hypothetical protein SBA6_80035 [Candidatus Sulfopaludibacter sp. SbA6]	2043166	Bacteria	Acidobacteria	Solibacteres	Solibacterales	Solibacteraceae	Candidatus Sulfopaludibacter	Candidatus Sulfopaludibacter sp. SbA6
BOT1cds2	WP_105313039.1	36.2	177	112	1	99	275	1	176	2.7e-22	115.5	179	275	64.4	WP_105313039.1 hypothetical protein [Candidatus Sulfopaludibacter sp. SbA6]	2043166	Bacteria	Acidobacteria	Solibacteres	Solibacterales	Solibacteraceae	Candidatus Sulfopaludibacter	Candidatus Sulfopaludibacter sp. SbA6
BOT1cds2	WP_048155622.1	28.2	280	187	7	3	275	6	278	4.6e-22	114.8	279	275	99.3	WP_048155622.1 MULTISPECIES: hypothetical protein [Methanosarcina]	2207;1434108;1860098	UNKNOWN/MULTIPLE	UNKNOWN/MULTIPLE	UNKNOWN/MULTIPLE	UNKNOWN/MULTIPLE	UNKNOWN/MULTIPLE	UNKNOWN/MULTIPLE	UNKNOWN/MULTIPLE
BOT1cds2	PKP60082.1	28.0	264	172	8	24	275	4	261	3.1e-18	102.1	266	275	91.6	PKP60082.1 hypothetical protein CVT88_04035 [Candidatus Altiarchaeales archaeon HGW-Altiarchaeales-1]	2013673	Archaea	Euryarchaeota	UNKNOWN	Candidatus Altiarchaeales	UNKNOWN	UNKNOWN	Candidatus Altiarchaeales archaeon HGW-Altiarchaeales-1
BOT1cds2	POZ52851.1	25.6	270	178	8	1	258	10	268	4.9e-08	68.2	295	275	93.8	POZ52851.1 hypothetical protein AADEFJLK_01460 [Methylovulum psychrotolerans]	1704499	Bacteria	Proteobacteria	Gammaproteobacteria	Methylococcales	Methylococcaceae	Methylovulum	Methylovulum psychrotolerans
BOT1cds2	WP_103973803.1	25.6	270	178	8	1	258	1	259	4.9e-08	68.2	286	275	93.8	WP_103973803.1 hypothetical protein [Methylovulum psychrotolerans]	1704499	Bacteria	Proteobacteria	Gammaproteobacteria	Methylococcales	Methylococcaceae	Methylovulum	Methylovulum psychrotolerans
"""


def test_version():
    assert __version__ == "0.1.0"


def test_annotate_diamond():
    taxdb_path = Path(os.environ.get('NCBI_TAX_DB', ''))
    if not(taxdb_path.exists() and taxdb_path.is_file()):
        pytest.skip("set NCBI_TAX_DB to the filename of a file containing the sqlite3 version of the NCBI taxonomy database")
    else:
        input_file = NamedTemporaryFile(mode='w+', delete=False)
        input_file.write(test_data)
        input_file.close()
        input_filename = input_file.name
        output_file = NamedTemporaryFile(mode='w+', delete=False)
        output_temp_filename = output_file.name
        diamond_output_format = "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore slen qlen qcovhsp stitle staxids"
        runner = CliRunner()
        runner.invoke(ncbi_taxid.cli.annotate_diamond,
                      ['--diamond_output_format', diamond_output_format,
                       '--output_file', output_temp_filename,
                       '--taxdb_filename', taxdb_path.as_posix(),
                       input_filename])

        os.unlink(input_filename)
        result = open(output_temp_filename).read()
        os.unlink(output_temp_filename)
        assert result == test_expected_result
