
const CyberShield = {

    state: {
        authenticated: false,
        currentModel: "Random Forest",
        uploadedFile: null,
        predictions: [],
        charts: {}
    },

    init() {

        this.cacheDOM();

        this.bindEvents();

        this.initializeDashboard();

        this.initializeCharts();

    },

    cacheDOM() {

        this.loginForm = document.getElementById("loginForm");

        this.username = document.getElementById("username");

        this.password = document.getElementById("password");

        this.loginMessage = document.getElementById("loginMessage");

        this.datasetInput = document.getElementById("datasetFile");

        this.predictionForm = document.getElementById("predictionForm");

        this.encryptButton = document.getElementById("encryptBtn");

        this.decryptButton = document.getElementById("decryptBtn");

        this.plainText = document.getElementById("plainText");

        this.output = document.getElementById("encryptedOutput");

    },

    bindEvents() {

        if (this.loginForm) {

            this.loginForm.addEventListener(
                "submit",
                this.handleLogin.bind(this)
            );

        }

        if (this.predictionForm) {

            this.predictionForm.addEventListener(
                "submit",
                this.handlePrediction.bind(this)
            );

        }

        if (this.datasetInput) {

            this.datasetInput.addEventListener(
                "change",
                this.handleFileUpload.bind(this)
            );

        }

        if (this.encryptButton) {

            this.encryptButton.addEventListener(
                "click",
                this.encryptText.bind(this)
            );

        }

        if (this.decryptButton) {

            this.decryptButton.addEventListener(
                "click",
                this.decryptText.bind(this)
            );

        }

    },

    initializeDashboard() {

        const metrics = document.querySelectorAll(".metric-card");

        metrics.forEach((card, index) => {

            card.style.animationDelay = `${index * 0.15}s`;

            card.classList.add("fade-in");

        });

    },

    handleLogin(event) {

        event.preventDefault();

        const username = this.username.value.trim();

        const password = this.password.value.trim();

        if (!username || !password) {

            this.showToast(
                "Please enter username and password.",
                "warning"
            );

            return;

        }

        if (
            username === "Divyanshu" &&
            password === "12345"
        ) {

            localStorage.setItem(
                "CyberShieldAuth",
                "true"
            );

            this.showToast(
                "Authentication Successful",
                "success"
            );

            setTimeout(() => {

                window.location.href = "dashboard.html";

            }, 1000);

        }

        else {

            this.showToast(
                "Invalid Credentials",
                "error"
            );

        }

    },
      handleFileUpload(event) {

        const file = event.target.files[0];

        if (!file) {

            return;

        }

        if (!file.name.toLowerCase().endsWith(".csv")) {

            this.showToast(
                "Only CSV files are supported.",
                "error"
            );

            event.target.value = "";

            return;

        }

        this.state.uploadedFile = file;

        this.showToast(
            `${file.name} selected successfully.`,
            "success"
        );

        this.readCSV(file);

    },

    readCSV(file) {

        const reader = new FileReader();

        reader.onload = (event) => {

            const content = event.target.result;

            const rows = content
                .trim()
                .split("\n");

            const columns = rows[0]
                .split(",");

            this.state.dataset = {

                rows: rows.length - 1,

                columns: columns.length,

                headers: columns

            };

            this.updateDatasetInfo();

        };

        reader.readAsText(file);

    },

    updateDatasetInfo() {

        const rows = document.getElementById("datasetRows");

        const cols = document.getElementById("datasetColumns");

        const model = document.getElementById("selectedModel");

        if (rows) {

            rows.textContent =
                this.state.dataset.rows;

        }

        if (cols) {

            cols.textContent =
                this.state.dataset.columns;

        }

        if (model) {

            model.textContent =
                this.state.currentModel;

        }

    },

    handlePrediction(event) {

        event.preventDefault();

        if (!this.state.uploadedFile) {

            this.showToast(
                "Please upload a dataset first.",
                "warning"
            );

            return;

        }

        this.showLoading();

        setTimeout(() => {

            this.hideLoading();

            this.generatePrediction();

        },2000);

    },

    generatePrediction() {

        const result = {

            accuracy:98.3,

            precision:97.8,

            recall:97.4,

            f1:97.6,

            threat:"DDoS"

        };

        this.state.predictions.push(result);

        this.updateDashboard(result);

        this.showToast(

            "Prediction completed successfully.",

            "success"

        );

    },
      async handlePrediction(event) {

        event.preventDefault();

        if (!this.state.uploadedFile) {

            this.showToast(
                "Please upload a CSV dataset first.",
                "warning"
            );

            return;

        }

        try {

            this.showLoading();

            const formData = new FormData();

            formData.append(
                "dataset",
                this.state.uploadedFile
            );

            formData.append(
                "model",
                this.state.currentModel
            );

            const response = await fetch(
                "/predict",
                {
                    method: "POST",
                    body: formData
                }
            );

            if (!response.ok) {

                throw new Error(
                    "Prediction request failed."
                );

            }

            const result = await response.json();

            this.state.predictions.push(result);

            this.updateDashboard(result);

            this.updateCharts(result);

            this.showToast(
                "Prediction completed successfully.",
                "success"
            );

        }

        catch (error) {

            console.error(error);

            this.showToast(
                "Unable to generate prediction.",
                "error"
            );

        }

        finally {

            this.hideLoading();

        }

    },

    updateDashboard(result) {

        const metrics = {

            threatScore:
                document.getElementById("threatScore"),

            packets:
                document.getElementById("packetCount"),

            accuracy:
                document.getElementById("accuracy"),

            predictionTime:
                document.getElementById("predictionTime"),

            attack:
                document.getElementById("highestThreat")

        };

        if(metrics.threatScore){

            metrics.threatScore.textContent =
                result.threat_score + "%";

        }

        if(metrics.packets){

            metrics.packets.textContent =
                result.total_packets;

        }

        if(metrics.accuracy){

            metrics.accuracy.textContent =
                result.accuracy + "%";

        }

        if(metrics.predictionTime){

            metrics.predictionTime.textContent =
                result.prediction_time + " ms";

        }

        if(metrics.attack){

            metrics.attack.textContent =
                result.highest_threat;

        }

    },
      updateCharts(result){

        if(
            this.state.charts.attackChart
        ){

            this.state.charts.attackChart.data.datasets[0].data =
                result.attack_distribution.values;

            this.state.charts.attackChart.update();

        }

        if(
            this.state.charts.featureChart
        ){

            this.state.charts.featureChart.data.labels =
                result.feature_importance.labels;

            this.state.charts.featureChart.data.datasets[0].data =
                result.feature_importance.values;

            this.state.charts.featureChart.update();

        }

    },

    initializeCharts(){

        const attackCanvas =
            document.getElementById("attackChart");

        if(attackCanvas){

            this.state.charts.attackChart =
                new Chart(attackCanvas,{

                    type:"doughnut",

                    data:{

                        labels:[],

                        datasets:[{

                            data:[],

                            backgroundColor:[
                                "#10B981",
                                "#EF4444",
                                "#F59E0B",
                                "#2563EB",
                                "#8B5CF6",
                                "#06B6D4"
                            ],

                            borderWidth:0

                        }]

                    },

                    options:{

                        responsive:true,

                        plugins:{
                            legend:{
                                labels:{
                                    color:"#F8FAFC"
                                }
                            }
                        }

                    }

                });

        }

        const featureCanvas =
            document.getElementById("featureChart");

        if(featureCanvas){

            this.state.charts.featureChart =
                new Chart(featureCanvas,{

                    type:"bar",

                    data:{

                        labels:[],

                        datasets:[{

                            label:"Importance",

                            data:[]

                        }]

                    },

                    options:{

                        responsive:true,

                        plugins:{
                            legend:{
                                display:false
                            }
                        }

                    }

                });

        }

    },
      showLoading(){

        let loader =
            document.getElementById("loadingOverlay");

        if(loader){

            loader.style.display="flex";

            return;

        }

        loader=document.createElement("div");

        loader.id="loadingOverlay";

        loader.className="loading-overlay";

        loader.innerHTML=`

            <div class="loader"></div>

        `;

        document.body.appendChild(loader);

    },

    hideLoading(){

        const loader=document.getElementById("loadingOverlay");

        if(loader){

            loader.remove();

        }

    },

    showToast(message,type="success"){

        const toast=document.createElement("div");

        toast.className=`toast ${type}`;

        toast.innerHTML=`

            <strong>${message}</strong>

        `;

        document.body.appendChild(toast);

        setTimeout(()=>{

            toast.remove();

        },3000);

    },

    encryptText() {

        if (!this.plainText || !this.output) {

            return;

        }

        const message = this.plainText.value.trim();

        if (message === "") {

            this.showToast(
                "Enter a message to encrypt.",
                "warning"
            );

            return;

        }

        const secretKey = "CyberShield2026";

        const encrypted = CryptoJS.AES.encrypt(

            message,
            secretKey

        ).toString();

        this.output.value = encrypted;

        this.showToast(
            "AES encryption completed.",
            "success"
        );

    },

    decryptText() {

        if (!this.output || !this.plainText) {

            return;

        }

        try {

            const secretKey = "CyberShield2026";

            const bytes = CryptoJS.AES.decrypt(

                this.output.value,

                secretKey

            );

            const decrypted = bytes.toString(

                CryptoJS.enc.Utf8

            );

            if (!decrypted) {

                throw new Error();

            }

            this.plainText.value = decrypted;

            this.showToast(

                "AES decryption completed.",

                "success"

            );

        }

        catch {

            this.showToast(

                "Unable to decrypt the message.",

                "error"

            );

        }

    },
      logout(){

        localStorage.removeItem(

            "CyberShieldAuth"

        );

        window.location.href="index.html";

    },

    checkAuthentication(){

        const auth=

        localStorage.getItem(

            "CyberShieldAuth"

        );

        if(

            window.location.pathname.includes(

                "dashboard"

            )

            &&

            auth!=="true"

        ){

            window.location.href="index.html";

        }

    },

    animateCounters(){

        const counters=

        document.querySelectorAll(

            "[data-count]"

        );

        counters.forEach(counter=>{

            const target=

            Number(

                counter.dataset.count

            );

            let value=0;

            const increment=

            Math.ceil(target/120);

            const timer=setInterval(()=>{

                value+=increment;

                if(value>=target){

                    value=target;

                    clearInterval(timer);

                }

                counter.textContent=value;

            },15);

        });

    }

};

document.addEventListener(

    "DOMContentLoaded",

    ()=>{

        CyberShield.checkAuthentication();

        CyberShield.init();

        CyberShield.animateCounters();

    }

);