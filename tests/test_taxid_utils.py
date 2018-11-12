import os
from pathlib import Path

import pytest

from diamond_add_taxonomy import __version__
from diamond_add_taxonomy.taxid_utils import TaxIDExpander


def test_version():
    assert __version__ == '0.1.0'


def taxdb_scientific_name(taxdb):
    # 51751 - Python regius
    scientific_name = taxdb.get_scientific_name(51751)
    assert scientific_name == 'Python regius'


def taxdb_lineage(taxdb: TaxIDExpander):
    # 51751 - Python regius
    lineage = taxdb.get_lineage('51751')
    assert ('phylum', 'Chordata') in lineage
    assert ('family', 'Pythonidae',) in lineage
    assert ('no rank', 'Sauropsida') in lineage
    lineage_standard = taxdb.get_lineage('51751', only_standard_ranks=True)
    assert len(lineage_standard) <= 7
    assert lineage_standard[0] == ('superkingdom', 'Eukaryota')
    assert lineage_standard[-1] == ('species', 'Python regius')


def test_load_from_db():
    taxdb_path = Path(os.environ.get('NCBI_TAX_DB', ''))
    if not (taxdb_path.exists() and taxdb_path.is_file()):
        pytest.skip("set NCBI_TAX_DB to the filename of a file containing the sqlite3 version of the NCBI taxonomy database")
    else:
        taxdb_filename = taxdb_path.as_posix()
        t = TaxIDExpander(taxdb_filename=taxdb_filename)
        taxdb_scientific_name(t)
        taxdb_lineage(t)


def test_load_from_taxdump():
    test_long_running = os.environ.get('TEST_LONG_RUNNING', False)
    if not test_long_running:
        pytest.skip("skip long running test")
    else:
        taxdump_path = Path(os.environ.get('NCBI_TAXDUMP_FILE', ''))
        if not (taxdump_path.exists() and taxdump_path.is_file()):
            pytest.skip("set NCBI_TAXDUMP_FILE to the filename of a file the taxdump.tar.gz from the NCBI taxonomy database")
        else:
            taxdump_filename = taxdump_path.as_posix()
            t = TaxIDExpander(taxdump_filename=taxdump_filename)
            taxdb_scientific_name(t)
            taxdb_lineage(t)


def test_load_from_net():
    test_long_running = os.environ.get('TEST_LONG_RUNNING', False)
    if not test_long_running:
        pytest.skip("skip long running test")
    else:
        t = TaxIDExpander()
        taxdb_scientific_name(t)
        taxdb_lineage(t)
