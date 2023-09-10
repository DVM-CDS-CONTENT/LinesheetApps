$Env:CONDA_EXE = "C:/Users/poojaroonwit/AppData/Local/miniconda3\Scripts\conda.exe"
$Env:_CE_M = ""
$Env:_CE_CONDA = ""
$Env:_CONDA_ROOT = "C:/Users/poojaroonwit/AppData/Local/miniconda3"
$Env:_CONDA_EXE = "C:/Users/poojaroonwit/AppData/Local/miniconda3\Scripts\conda.exe"
$CondaModuleArgs = @{ChangePs1 = $True}
Import-Module "$Env:_CONDA_ROOT\shell\condabin\Conda.psm1" -ArgumentList $CondaModuleArgs

Remove-Variable CondaModuleArgs