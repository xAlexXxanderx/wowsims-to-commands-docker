window.onload = function () {
    const form = document.getElementById('form');
    form.addEventListener('submit', onFormSubmit);
}

async function onFormSubmit(event) {
    event.preventDefault();
    console.group('Javascript: Setting input parameters');
    console.log('Button clicked, working...');

    // No Text Area validation, let python handle it
    // let inputTextArea = document.getElementById("inputTextArea");

    let spinner = document.getElementById('spinner');
    let button = document.getElementById('formButton');
    let outputTxtArea = document.getElementById('outputTextArea');

    // Decide on Input and Output name based on radio button
    let inputDfSpellFilename = "./web/data/df_spell.pkl";
    let inputDfItemFilename = "./web/data/df_item.pkl";
    console.log(`Input spell df: ${inputDfSpellFilename}`);
    console.log(`Input item df: ${inputDfItemFilename}`);
    console.groupEnd('Javascript: Setting input parameters');

    // Load script
    const pythonScriptPath = "./web/python/script.py";
    const script = await (await fetch(pythonScriptPath)).text();

    // Load df_spell
    blobSpell = await (await fetch(inputDfSpellFilename)).blob();
    const arrayBufferSpell = await blobSpell.arrayBuffer();
    inputDfSpell = arrayBufferSpell

    // Load df_item
    blobItem = await (await fetch(inputDfItemFilename)).blob();
    const arrayBufferItem = await blobItem.arrayBuffer();
    inputDfItem = arrayBufferItem

    try {
        console.log(`Loading Pyodide...`);
        spinner.style.visibility = 'visible';
        button.disabled = true;
        outputTxtArea.value = '';
        // Load Pyodide
        let pyodide = await loadPyodide();
        // Install Pandas with micropip
        // https://pyodide.org/en/stable/usage/loading-packages.html
        await pyodide.loadPackage("micropip");
        const micropip = pyodide.pyimport("micropip");
        await micropip.install("pandas");
        // Run script
        console.log(`Running Python script`);
        await pyodide.runPythonAsync(script);
        spinner.style.visibility = 'hidden';
        button.disabled = false;
    }
    catch (err) {
        spinner.style.visibility = 'hidden';
        button.disabled = false;
        outputTxtArea.value = err;
        console.log(err);
    }
}
