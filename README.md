# Orchidokie

Orchidokie uses the [ORCID API](https://orcid.org/organizations/integrators/API) (version 2.0) to list the datasets associated with a journal article, conference paper, or other publication.

The tool requires the dataset's ORCID record to contain (in the `Work Identifiers` section of the metadata):

1. The DOI of the dataset itself, marked as `Self`.
2. The DOI of the associated publication, marked as `Part of`.

This is so far only a prototype aimed a highlighting how good metadata practices can help with data discovery.

## Dependencies

The tool relies heavily on a Python implementation of the ORCID API, which can be obtained from GitHub and installed using the following commands:

```
git clone https://github.com/ORCID/python-orcid.git
cd python-orcid
git checkout 2.0update
sudo python setup.py install
```

Note the switch to the `2.0update` branch.

## Setup

A "Client ID" and a "Client Secret" are required. These can be obtained by creating a new application in the [Developer Tools](https://orcid.org/developer-tools) section of the ORCID website. They should be passed in at the command line, along with the DOI of the publication:

```
python orchidokie.py client_id_here client_secret_here 10.000/doi.123.here
```

## Example

```
christian@banoffee ~/orchidokie $ python orchidokie.py CLIENT_ID_HIDDEN CLIENT_SECRET_HIDDEN 10.1016/j.jocs.2016.11.001
Datasets of 10.1016/j.jocs.2016.11.001:

	 * Enstrophy and kinetic energy data from 3D Taylor-Green vortex simulations (https://doi.org/10.5258/SOTON/401892)
```

## License

Orchidokie is released under the MIT license. See the `LICENSE` file for more information.
