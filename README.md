[![Abcdspec-compliant](https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg)](https://github.com/brain-life/abcd-spec)
[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-bl.app.53-blue.svg)](https://doi.org/10.25663/bl.app.53)

# app-wmctotrk
This App converts a WMC brainlife.io DataType to a TRK file.

### Authors
- David Hunt (davhunt@iu.edu)
- Paolo Avesani (avesani@fbk.eu)

### Contributors
- Soichi Hayashi (hayashi@iu.edu)
- Franco Pestilli (franpest@indiana.edu)

### Funding
[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)

## Running the App 

### On Brainlife.io

You can submit this App online at [https://doi.org/10.25663/bl.app.127](https://doi.org/10.25663/bl.app.127) via the "Execute" tab.

### Running Locally (on your machine)

1. git clone this repo.
2. Inside the cloned directory, create `config.json` with something like the following content with paths to your input files.

```json
{
  "wmc": "./wmc.mat",
	"t1": "./t1.nii" 

}
```

### Sample Datasets

You can download sample datasets from Brainlife using [Brainlife CLI](https://github.com/brain-life/cli).

```
npm install -g brainlife
bl login
mkdir input
ADD HERE

```


3. Launch the App by executing `main`

```bash
./main
```

## Output

The main output of this App is dt6.mat structure that can be used in any apps requiring a dtiinit input.

#### Product.json
The secondary output of this app is `product.json`. This file allows web interfaces, DB and API calls on the results of the processing. 

### Dependencies

This App requires the following libraries when run locally.

  - singularity: https://singularity.lbl.gov/
  - FSL: https://hub.docker.com/r/brainlife/fsl/tags/5.0.9
  - Dipy: https://hub.docker.com/r/brainlife/dipy/tags/0.13.0
  - jsonlab: https://github.com/fangq/jsonlab.git

