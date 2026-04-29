cwlVersion: v1.2
class: CommandLineTool
label: Tool to sobel image
requirements:
  ShellCommandRequirement: {}
  InlineJavascriptRequirement: {}
inputs:
  script:
    type: File
  images:
    type:
      type: array
      items: File
arguments:
  - shellQuote: false
    valueFrom: >
      ${
        var cmd = "";
        for(var i = 0; i < inputs.images.length; i++) {
            cmd += ["\n python3",
              inputs.script.path,
              inputs.images[i].location,
              inputs.images[i].basename,
            ].join(" ");
        }
        return cmd;
      }
outputs:
  standard_output:
    type: stdout
  standard_error:
    type: stderr
  output_files:
    type:
      type: array
      items: File
    outputBinding:
      glob: '*.jpeg'
stdout: binarize_stdout.txt
stderr: binarize_stderr.txt
