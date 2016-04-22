; The name of the installer
Name "Inkscape-music-scale-generator"

; The file to write
OutFile "Inkscape-music-scale-generator.exe"

; I'm not sure how to get an actual installation directory of the Inkscape,
; therefore we'll install extension files into the user's appdata roaming folder
InstallDir $APPDATA\Inkscape

;--------------------------------

; Pages
Page directory
Page instfiles

;--------------------------------

; The stuff to install
Section "" ;No components page, name is not important

  ; Set output path to the installation directory.
  SetOutPath $INSTDIR\extensions
  
  ; Put file there
  File ..\share\extensions\svgPianoScale.inx 
  File ..\share\extensions\svgPianoScale.py
  
  SetOutPath $INSTDIR\examples
  
  File ..\share\examples\MajorScales.svg 
  
SectionEnd ; end the section