const fetch = require("node-fetch");
const fs = require("fs");
const path = require("path");

async function fetchData(conversation_id) {
  const polis_api_host = "https://polis.japanchoice.jp/api"; // 必要に応じて設定
  const acceptLang = "en"; // 必要に応じて設定

  try {
    const response = await fetch(
      `${polis_api_host}/v3/participationInit?conversation_id=${conversation_id}&pid=mypid&lang=${acceptLang}`,
      { credentials: "include" }
    );
    const participation_init = await response.json();

    const now = new Date().toISOString().replace(/:/g, "-");
    const filePath = path.join(
      __dirname,
      "data",
      `${conversation_id}-${now}.json`
    );

    // ディレクトリがなければ作成
    if (!fs.existsSync(path.dirname(filePath))) {
      fs.mkdirSync(path.dirname(filePath), { recursive: true });
    }

    fs.writeFileSync(filePath, JSON.stringify(participation_init, null, 2));
    console.log("Saved to", filePath);
  } catch (err) {
    console.error("Error fetching data:", err);
  }
}

fetchData("69rmeiumcr");
fetchData("42pditmrma");
fetchData("77anwcwh4b");
fetchData("35r8w9kkfp");
fetchData("32ffrfvrrf");
fetchData("3dzkftnmrm");
fetchData("3zwj5fwytm");
