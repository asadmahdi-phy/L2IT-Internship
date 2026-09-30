import json
import json
import argparse
from pathlib import Path
import sys
import os

import json
import argparse
from pathlib import Path
import sys
import os

import lisabeta
import lisabeta.pyconstants as pyconstants
import lisabeta.tools.pytools as pytools

from astropy.cosmology import Planck15 as cosmo

def generate_json_files(output_dir, base_name, cut_f_name, max_f, M, Mchirp_inj, dxi0v_inj, dist, alpha_tape, wf_name, source_params=None, run_params=None):

    if wf_name == "PhenomD": 
        fref_for_phiref = 0.01
        fref_for_tref   = 0.01
        approximant = "IMRPhenomD"
        
    else: 
        fref_for_phiref = 0.0
        fref_for_tref   = 0.0  
        if wf_name == 'SEOBv5':
            approximant = 'SEOBNRv5HMROM'
        elif wf_name == 'SEOBv4':
            approximant = 'SEOBNRv4HMROM'
        elif wf_name == 'XHM':
            approximant = 'IMRPhenomXHM'

    base_name = f'{base_name}_{wf_name}'
    base_name_signal = base_name

    if alpha_tape == 0.5:
        base_name = f'{base_name}_alpha05'
    elif alpha_tape == 0.7:
        base_name = f'{base_name}_alpha07'
    elif alpha_tape == 0.9:
        base_name = f'{base_name}_alpha09'

    # Create the directory for the run
    base_pe_dir = Path("/pbs/home/a/amahdi/PE for my work")
    
    # output_dir comes from the function argument.
    # If output_dir = ".", files are saved directly inside "PE for my work".
    # If output_dir = "FTI_recovery_task", files are saved inside that subfolder.
    output_base_dir = base_pe_dir / output_dir
    
    directory_config = output_base_dir / "config_files" / base_name
    directory_config.mkdir(parents=True, exist_ok=True)
    
    directory_run = output_base_dir / "run_data" / base_name
    directory_run.mkdir(parents=True, exist_ok=True)
            
    base_config = {
        "source_params": {            
            "M": M,
            "q": 3,
            "chi1": -0.45,
            "chi2": 0.2,
            "Deltat": 0.0,
            "dist": dist,
            "inc": 2.412736486705947,
            "phi": 0.5251100790298958,
            "lambda": -2.552289318145636,
            "beta": -0.34932495086928644,
            "psi": 1.4013758013368807,
            "Lframe": True,
            "fti_dchiMinus2v": 0,
        },
        "waveform_params": {
            "minf": 1e-5,
            "maxf": max_f,
            "t0": 0.0,
            "timetomerger_max": 1.0,
            "fend": None,
            "tmin": None,
            "tmax": None,
            "phiref": 0.0,
            "fref_for_phiref": fref_for_phiref,
            "tref": 0.0,
            "fref_for_tref": fref_for_tref,
            "force_phiref_fref": True,
            "toffset": 0.0,
            "modes": None,
            "TDI": "TDIAET",
            "acc": 1e-4,
            "order_fresnel_stencil": 0,
            "approximant": approximant,
            "LISAconst": "Proposal",
            "responseapprox": "full",
            "frozenLISA": False,
            "TDIrescaled": True,
            "LISAnoise": {
                "InstrumentalNoise": "SciRDv1",
                "WDbackground": True,
                "WDduration": 4.0,
                "lowf_add_pm_noise_f0": 0.0,
                "lowf_add_pm_noise_alpha": 2.0
            },
            "tgr_params": {
                "FTI": {
                    "fti_params": [
                        "fti_dchiMinus2v", "fti_dchi0v", "fti_dchi1v", "fti_dchi2v",
                        "fti_dchi3v", "fti_dchi4v", "fti_dchi5lv", "fti_dchi6v",
                        "fti_dchi6lv", "fti_dchi7v", "fti_dkappa_S", "fti_dxi0v"
                    ],
                    'f_window_div_f_peak': alpha_tape, 
                    'Mchirp_inj': Mchirp_inj, 
                    'dxi0v_inj': dxi0v_inj
                }
            }
        },
        "prior_params": {
            "list_params": [
                "Mchirp", "q", "chiPN", "chim", "Deltat", "dist", "inc", "phi",
                "lambda", "beta", "psi", "fti_dchiMinus2v"
            ],
            "infer_params": [
                "Mchirp", "q", "chiPN", "chim", "Deltat", "dist", "inc", "phi",
                "lambda", "beta", "psi", "fti_dchiMinus2v"
            ],
            "params_range": [
                [0.1*M, 10*M], [1, 10], [-0.99, 0.99], [-0.99, 0.99],
                [-600.0, 600.0], [2863.0, 25924], [], [], [], [], [], [-30, 30]
            ],
            "prior_type": [
                "uniform", "uniform", "uniform", "uniform", "uniform", "uniform",
                "sin", "uniform", "uniform", "cos", "uniform", "uniform"
            ], 
            "extra_prior_bounds": {"chi1": [-0.99, 0.99], "chi2": [-0.99, 0.99]},
            "wrap_params": None
        },

        "run_params": {
            "out_dir": str(directory_run) + "/",
            "out_name": "",
            "sampler": "ptemcee",
            "sample_Lframe": True,
            "multimodal": True,
            "multimodal_pattern": "8modes",
            "p_jump": 0.5,
            "likelihood_method": "fresnel",
            # "data_file": f"/work/LISA/piarulm/FTI/PE_analysis/tdi_injections/signal_{base_name_signal}.h5",
            "likelihood_residuals_ngrid": 128,
            "skip_fisher": False,
            "init_method": "fisher",
            "init_fisher_options": {"fisher_params": ["Mchirp", "q", "chiPN", "chim", "Deltat", "dist", "inc", "phi",
                "lambda", "beta", "psi", "fti_dchiMinus2v"]},
            "init_scale_cov": 100,
            "zerolike": False,
            "n_temps": 10,
            "temp_max": None,
            "n_walkers": 64,
            "n_iter": 10000,
            "burn_in": 5000,
            "autocor_method": "autocor_new",
            "thin_samples": True,
            "upsample": 1,
            "seed": None,
            "print_info": True,
            "n_iter_info": 50,
            "output": True,
            "output_raw": True
        }
    }

    # Update source_params if provided
    if source_params:
        base_config["source_params"].update(source_params)

    # Update run_params if provided
    if run_params:
        base_config["run_params"].update(run_params)

    fti_params = [
        "fti_dchiMinus2v", "fti_dchi0v", "fti_dchi1v", "fti_dchi2v",
        "fti_dchi3v", "fti_dchi4v", "fti_dchi5lv", "fti_dchi6v",
        "fti_dchi6lv", "fti_dchi7v", "fti_dkappa_S", "fti_dxi0v"
    ]

    for param in fti_params:

        config = base_config.copy()
        sp = config["source_params"].copy()
        sp.popitem()  # removes the last added item (assumes it's always the fti param)
        sp[param] = 0  # add current param with default value
        
        config["source_params"] = sp
        config["prior_params"]["list_params"][-1] = param
        config["prior_params"]["infer_params"][-1] = param
        config["run_params"]["init_fisher_options"]["fisher_params"][-1] = param
        config["run_params"]["out_name"] = f"{base_name}_{param}_{cut_f_name}"

        output_file = directory_config / f"{base_name}_{param}_{cut_f_name}.json"
        try:
            with open(output_file, "w") as f:
                json.dump(config, f, indent=2)
            print(f"Generated {output_file}")
        except PermissionError:
            print(f"Error: Permission denied when trying to write to {output_file}")
            print("Please make sure you have write permissions for the output directory.")
            sys.exit(1)
        except OSError as e:
            print(f"Error: Unable to write to {output_file}")
            print(f"OS error: {e}")
            sys.exit(1)

def parse_dict_arg(arg):
    if not arg:
        return {}
    try:
        return json.loads(arg)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in argument: {arg}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate waveform JSON files")
    parser.add_argument("output_dir", type=str, help="Output directory for JSON files")
    parser.add_argument("base_name", type=str, help="Base name for output files")
    parser.add_argument("cut_f_name", type=str, help="IMR - ISCO - 22peak - 22tape", default = "IMR")
    parser.add_argument("M", type=float, help="mass_tot", default = 1e6)  
    parser.add_argument("Mchirp_inj", type=float, help="chirp mass", default = 1e6) 
    parser.add_argument("dxi0v_inj", type=float, help="dxi0", default = 0)
    parser.add_argument("max_f", type=float, help="max_f value", default = 0.5)
    parser.add_argument("z", type=float, help="redshift", default = 1)
    parser.add_argument("alpha_tape", type=float, help="tapering point", default = 0.35)
    parser.add_argument("wf_name", type=str, help="XHM, SEOBv5")
    parser.add_argument("--source_params", type=str, help="JSON string of source parameters to override")
    parser.add_argument("--run_params", type=str, help="JSON string of run parameters to override")
    args = parser.parse_args()

    # output_dir = Path(args.output_dir).resolve()
#     if not output_dir.is_dir():
#         print(f"Error: The specified output directory does not exist: work/LISA/piarulm/FTI/PE_analysis/{output_dir}")
#         sys.exit(1)

#     if not os.access(output_dir, os.W_OK):
#         print(f"Error: You do not have write permissions for the directory: work/LISA/piarulm/FTI/PE_analysis/{output_dir}")
#         sys.exit(1)

    source_params = parse_dict_arg(args.source_params)
    run_params = parse_dict_arg(args.run_params)
    
    z = args.z
    dist = cosmo.luminosity_distance(z).value
    
    generate_json_files(args.output_dir, args.base_name, args.cut_f_name, args.max_f, args.M, args.Mchirp_inj, args.dxi0v_inj, dist, args.alpha_tape, args.wf_name, source_params, run_params)