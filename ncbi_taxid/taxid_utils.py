from pathlib import Path
from typing import Optional, List, Tuple
from ete3 import NCBITaxa


class TaxIDExpander(object):

    def __init__(self, taxdump_filename: str = None, taxdb_filename: str = None) -> 'TaxIDExpander':
        """Constructor for TaxIDExpander

        Args:
            taxdump_filename(str): if specified, refers to a local copy of the NCBI taxdump.tar.gz file
            taxdb_filename(str): if specified will be used to look for a db containing the NCBI database to load.
                                 if both taxdump_filename and taxdb_filename are set, save to taxdb_filename """
        if taxdump_filename is not None:
            taxdump_path = Path(taxdump_filename)
            if not (taxdump_path.exists() and taxdump_path.is_file()):
                raise ValueError(f'{taxdump_filename} must be a readable file')
            if taxdb_filename is not None:
                # we have both a taxdump file and a taxdb file
                # this means we load from taxdump file and save to taxdb file
                self.ncbi = NCBITaxa(taxdump_file=taxdump_filename, dbfile=taxdb_filename)
            else:
                # we have a taxdump file and no taxdb file
                # this means we load from the taxdump file and let ete3 save to its default location
                self.ncbi = NCBITaxa(taxdump_file=taxdump_filename)
        else:
            if taxdb_filename is not None:
                # we have a taxdb file and no taxdump file
                # this means we load the database from the taxdb file
                taxdb_path = Path(taxdb_filename)
                if not (taxdb_path.exists() and taxdb_path.is_file()):
                    raise ValueError(f'{taxdb_filename} must be a readable file')
                self.ncbi = NCBITaxa(dbfile=taxdb_filename)
            else:
                # we have neither a taxdump file nor a taxdb file
                # this means ete3 loads the database over the network (and cache in local directory)
                # and let ete3 save the taxdb to its default location
                self.ncbi = NCBITaxa()

    def get_lineage(self, taxid: str, only_standard_ranks: Optional[bool] = False) -> List[Tuple[str, str]]:
        """Return lineage for a given taxonomy ID

        Raises ValueError if taxonomy ID is not found.

        Args:
            taxid(str): NCBI taxonomy ID
            only_standard_ranks(bool): if True only return superkingdom, phylum, class, order, family, genus and species ranks
        Returns:
            list of tuples where the tuples have members (taxon rank, taxon name)"""
        lineage_ids = self.ncbi.get_lineage(taxid)
        names = self.ncbi.get_taxid_translator(lineage_ids)
        ranks = self.ncbi.get_rank(lineage_ids)
        standard_ranks = set(['superkingdom', 'phylum', 'class',
                              'order', 'family', 'genus', 'species'])
        lineage = []
        for id in lineage_ids:
            rank = ranks[id]
            if only_standard_ranks and rank not in standard_ranks:
                continue
            lineage.append((ranks[id], names[id]))
        return lineage

    def get_scientific_name(self, taxid: str):
        results = self.ncbi.translate_to_names([taxid])
        if not results:
            return 'UNKNOWN'
        else:
            return results[0]
