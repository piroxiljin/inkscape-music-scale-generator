; The name of the installer
Name "Inkscape-music-scale-generator"

; The file to write
OutFile "Inkscape-music-scale-generator.exe"

; The only place where I have found reliable path to the Inkscape is uninstall-key from regestry
InstallDirRegKey HKLM SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Inkscape InstallLocation

; Request application privileges for Windows Vista
RequestExecutionLevel admin

;--------------------------------

; Pages

Page directory
Page instfiles

;--------------------------------

; The stuff to install
Section "" ;No components page, name is not important

  ; Set output path to the installation directory.
  SetOutPath $INSTDIR\share\extensions
  
  ; Put file there
  File ..\share\extensions\svgPianoScale.inx 
  File ..\share\extensions\svgPianoScale.py
  
  SetOutPath $INSTDIR\share\examples
  
  File ..\share\examples\MajorScales.svg 
  
SectionEnd ; end the section