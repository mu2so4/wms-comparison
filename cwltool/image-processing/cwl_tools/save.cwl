cwlVersion: v1.2
class: CommandLineTool
label: Tool to save images
requirements:
  ShellCommandRequirement: {}
  InlineJavascriptRequirement: {}
inputs:
  images:
    type:
      type: array
      items: File
  output_dir:
    type: Directory
arguments:
  - shellQuote: false
    valueFrom: >
      ${
        var cmd = "";
        for(var i = 0; i < inputs.images.length; i++) {
            cmd += ["\n mv",
              inputs.images[i].location,
              inputs.output_dir.location + "/" + inputs.images[i].basename,
            ].join(" ");
        }
        return cmd;
      }
outputs:
  output_files:
    type:
      type: array
      items: File
    outputBinding:
      glob: '*.jpeg'
