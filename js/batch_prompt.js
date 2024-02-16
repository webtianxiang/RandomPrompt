import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

app.registerExtension({
  name: "TX.BatchPromptMenu",
  setup() {
    const menu = document.querySelector(".comfy-menu");
    const separator = document.createElement("hr");

    separator.style.margin = "20px 0";
    separator.style.width = "100%";
    menu.append(separator);

    const BatchPromptButton = document.createElement("button");
    BatchPromptButton.textContent = "Tx Batch Prompt";
    BatchPromptButton.onclick = () => {
      for (let i = 0; i < 3; i++) {
        app.queuePrompt(0, this.batchCount);
      }
      alert("Tx Batch Prompt 3");
    };
    menu.append(BatchPromptButton);

    const BatchDownloadButton = document.createElement("button");
    BatchDownloadButton.textContent = "Batch Download";
    BatchDownloadButton.onclick = () => {
      api
        .fetchApi("/tx/batch-download", {
          method: "POST",
          headers: { "Content-Type": "application/zip" },
          body: "",
        })
        .then((resp) => resp.blob())
        .then((blob) => {
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.style.display = "none";
          a.href = url;
          a.download = "result.zip";
          document.body.appendChild(a);
          a.click();
          window.URL.revokeObjectURL(url);
          alert("your file has downloaded!");
        });
    };
    menu.append(BatchDownloadButton);
  },
});
