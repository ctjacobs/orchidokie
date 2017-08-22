#!/usr/bin/env python

# Orchidokie is released under the MIT license.

# The MIT License (MIT)

# Copyright (c) 2017 Christian T. Jacobs

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import orcid
import argparse


class Orchidokie:

    """ Finds all datasets associated with a publication (e.g. a journal article or conference paper) with a given Digital Object Identifier (DOI). """

    def __init__(self, client_id, client_secret):
        """ Set up the ORCID API and retrieve a search token. """
        self.api = orcid.PublicAPI(client_id, client_secret, sandbox=False)
        self.search_token = self.api.get_search_token_from_orcid()

    def find_datasets(self, doi):
        """ Return the datasets associated with a publication with a given DOI.

        :arg str doi: The DOI of the publication.
        :rtype: list
        :returns: The list of datasets.
        """

        search_results = self.api.search("doi-part-of:%s" % doi, access_token=self.search_token)

        datasets = []

        for r in search_results["result"]:  # For each ORCID that contains work(s) associated with this DOI...
            author_orcid = r["orcid-identifier"]["path"]  # Get the ORCID.

            # Read the ORCID and get all the works.
            summary = self.api.read_record_public(author_orcid, 'works', self.search_token)
            # Now find the publication and its associated datasets that we seek.
            for work in summary["group"]:  # For each work in the group...
                for source in work["work-summary"]:  # For each source...
                    if(source["type"].upper() == "DATA_SET"):
                        dataset = {}
                        partof = False
                        for e in source["external-ids"]["external-id"]:  # For each external ID...
                            if(e["external-id-type"] == "doi"):
                                if(e["external-id-relationship"].upper() == "PART_OF" and e["external-id-value"] == doi):
                                    # This is a dataset associated with the publication.
                                    partof = True
                                    dataset["title"] = source["title"]["title"]["value"]
                                elif(e["external-id-relationship"].upper() == "SELF"):
                                    if(not e["external-id-url"]):
                                        dataset["external-id-url"] = "https://doi.org/" + e["external-id-value"]
                                    else:
                                        dataset["external-id-url"] = e["external-id-url"]["value"]

                        if(partof and not self.is_duplicate(dataset, datasets)):
                            # Only append if the dataset is a part of the publication and doesn't already exist in the list of datasets.
                            datasets.append(dataset)

        return datasets

    def is_duplicate(self, dataset, datasets):
        """ Determine whether the dataset already exists in the list of datasets.

        :arg dict dataset: The dataset under consideration.
        :arg list datasets: The list of datasets to check against.
        :rtype: bool
        :returns: True if the dataset already exists, and False otherwise.
        """
        for d in datasets:
            if(d["external-id-url"] == dataset["external-id-url"]):
                return True
        return False

    def print_datasets(self, doi, datasets):
        """ Print the list of datasets in a pretty way. """
        print "Datasets of %s:\n" % doi
        for d in datasets:
            print "\t * %s (%s)\n" % (d["title"], d["external-id-url"])
        return

if(__name__ == "__main__"):
    parser = argparse.ArgumentParser(prog="orchidokie", description="Lists the datasets associated with a specified publication on ORCID.")
    parser.add_argument("client_id", help="The client ID.", action="store", type=str)
    parser.add_argument("client_secret", help="The client secret.", action="store", type=str)
    parser.add_argument("doi", help="The DOI for the publication. This could be the DOI to a journal article or conference paper, for example", action="store", type=str)
    args = parser.parse_args()

    o = Orchidokie(args.client_id, args.client_secret)
    datasets = o.find_datasets(args.doi)
    o.print_datasets(args.doi, datasets)
