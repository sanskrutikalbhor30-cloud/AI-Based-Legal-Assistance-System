// ===============================
// LEGAL CATEGORY GUIDANCE
// ===============================

function showGuidance() {

    let category = document.getElementById("category").value;

    let guidance = "";
    let documents = "";
    let department = "";
    let step = "";
    let procedure = "";

    if (category === "Family Law") {

        guidance = "Family Law covers marriage, divorce, child custody and maintenance.";

        documents =
            "<li>Identity Proof</li>" +
            "<li>Address Proof</li>" +
            "<li>Marriage Certificate, where applicable</li>";

        department = "Family Court";

        step = "Collect all required documents and consult a family lawyer if needed.";

        procedure =
            "<li>Collect all required documents.</li>" +
            "<li>Organize the relevant records.</li>" +
            "<li>Consult a qualified family lawyer.</li>" +
            "<li>Take further legal action if required.</li>";

    }

    else if (category === "Property Law") {

        guidance = "Property Law deals with property ownership, registration and disputes.";

        documents =
            "<li>Property Documents</li>" +
            "<li>Ownership Records</li>" +
            "<li>Identity Proof</li>";

        department = "Sub-Registrar Office";

        step = "Collect and verify the relevant property documents.";

        procedure =
            "<li>Collect property documents.</li>" +
            "<li>Verify ownership records.</li>" +
            "<li>Consult a qualified legal professional.</li>" +
            "<li>Take appropriate legal action if required.</li>";

    }

    else if (category === "Cyber Crime") {

        guidance = "Cyber Crime includes online fraud, hacking and cyber complaints.";

        documents =
            "<li>Screenshots of Evidence</li>" +
            "<li>Bank Transaction Details</li>" +
            "<li>Mobile Number</li>" +
            "<li>Email Details</li>";

        department = "Cyber Crime Police Station";

        step = "Preserve the evidence and report the incident through the appropriate cyber-crime reporting channel.";

        procedure =
            "<li>Save screenshots and other evidence.</li>" +
            "<li>Collect transaction details.</li>" +
            "<li>Report the incident through the appropriate official channel.</li>" +
            "<li>Contact the Cyber Crime Police Station if required.</li>";

    }

    else if (category === "Consumer Law") {

        guidance = "Consumer Law deals with problems related to products and services.";

        documents =
            "<li>Purchase Bill</li>" +
            "<li>Warranty Documents</li>" +
            "<li>Payment Receipt</li>";

        department = "Consumer Commission";

        step = "Collect your purchase and complaint-related documents.";

        procedure =
            "<li>Keep the purchase bill.</li>" +
            "<li>Collect warranty and payment records.</li>" +
            "<li>Contact the seller or service provider.</li>" +
            "<li>Consider a consumer complaint if required.</li>";

    }

    else if (category === "Employment Law") {

        guidance = "Employment Law deals with various workplace-related legal matters.";

        documents =
            "<li>Employment Records</li>" +
            "<li>Salary Slips</li>" +
            "<li>Appointment Letter</li>";

        department = "Labour Office";

        step = "Collect your employment-related records.";

        procedure =
            "<li>Collect employment records.</li>" +
            "<li>Keep copies of relevant communications.</li>" +
            "<li>Discuss the issue through appropriate workplace channels.</li>" +
            "<li>Seek professional legal guidance if required.</li>";

    }

    else {

        guidance = "Please select a legal category.";
        documents = "";
        department = "";
        step = "";
        procedure = "";
    }


    document.getElementById("guidance").innerHTML = guidance;
    document.getElementById("documents").innerHTML = documents;
    document.getElementById("department").innerHTML = department;
    document.getElementById("step").innerHTML = step;
    document.getElementById("procedure").innerHTML = procedure;
}


// ===============================
// SEARCH LEGAL CATEGORY
// ===============================

function searchCategory() {

    let search = document.getElementById("searchCategory").value.trim();

    let category = document.getElementById("category");

    if (search.toLowerCase().includes("family")) {
        category.value = "Family Law";
    }

    else if (search.toLowerCase().includes("property")) {
        category.value = "Property Law";
    }

    else if (search.toLowerCase().includes("cyber") ||
             search.toLowerCase().includes("crime")) {
        category.value = "Cyber Crime";
    }

    else if (search.toLowerCase().includes("consumer")) {
        category.value = "Consumer Law";
    }

    else if (search.toLowerCase().includes("employment")) {
        category.value = "Employment Law";
    }

    else {
        alert("Legal category not found.");
        return;
    }

    showGuidance();
}


// ===============================
// LOGOUT USER
// ===============================

function logoutUser() {
    alert("You have been logged out successfully!");
    window.location.href = "/login";
}


// ===============================
// UPDATE NAVIGATION
// ===============================

function updateNavigation() {

    let savedUser = localStorage.getItem("legalUser");

    let loginLink = document.getElementById("loginLink");
    let registerLink = document.getElementById("registerLink");
    let logoutLink = document.getElementById("logoutLink");

    if (loginLink && registerLink && logoutLink) {

        if (savedUser !== null) {

            loginLink.style.display = "none";
            registerLink.style.display = "none";
            logoutLink.style.display = "inline";

        } else {

            loginLink.style.display = "inline";
            registerLink.style.display = "inline";
            logoutLink.style.display = "none";
        }
    }
}

// ======================================
// AI LEGAL RISK ANALYZER
// ======================================

function analyzeRisk() {

    let category = document.getElementById("riskCategory").value;
    let situation = document.getElementById("riskSituation").value.trim();
    let result = document.getElementById("riskResult");

    // Check category
    if (category === "") {
        alert("Please select a legal category.");
        return;
    }

    // Check situation
    if (situation === "") {
        alert("Please describe your situation.");
        return;
    }

    let riskLevel = "";
    let explanation = "";
    let action = "";

    // Cyber Crime
    if (category === "Cyber Crime") {

    let situationText = situation.toLowerCase();

    // HIGH RISK
    if (
        situationText.includes("hacked") ||
        situationText.includes("hack") ||
        situationText.includes("stolen") ||
        situationText.includes("money transferred") ||
        situationText.includes("bank account") ||
        situationText.includes("online fraud")
    ) {
        riskLevel = "HIGH RISK";
        explanation = "This situation may involve a serious cyber-related legal issue.";
        action = "Keep evidence such as messages, transaction details and screenshots and consider reporting the matter to the appropriate authorities.";
    }

    // MEDIUM RISK
    else if (
        situationText.includes("suspicious") ||
        situationText.includes("phishing") ||
        situationText.includes("link") ||
        situationText.includes("bank details") ||
        situationText.includes("password")
    ) {
        riskLevel = "MEDIUM RISK";
        explanation = "This situation may involve a potential cyber-related risk.";
        action = "Do not share personal information and keep the suspicious messages or communication as evidence.";
    }

    // LOW RISK
    else {
        riskLevel = "LOW RISK";
        explanation = "This appears to be a general cyber-safety query.";
        action = "Follow basic online safety practices and protect your personal information.";
    }
}

    // Family Law
    else if (category === "Family Law") {

    let situationText = situation.toLowerCase();

    // HIGH RISK
    if (
        situationText.includes("threat") ||
        situationText.includes("violence") ||
        situationText.includes("abuse") ||
        situationText.includes("danger") ||
        situationText.includes("domestic violence")
    ) {
        riskLevel = "HIGH RISK";
        explanation = "This situation may involve a serious family-related legal issue.";
        action = "Keep relevant evidence and consider seeking qualified legal guidance.";
    }

    // MEDIUM RISK
    else if (
        situationText.includes("divorce") ||
        situationText.includes("custody") ||
        situationText.includes("maintenance") ||
        situationText.includes("separation") ||
        situationText.includes("child")
    ) {
        riskLevel = "MEDIUM RISK";
        explanation = "This situation may involve a family-related legal dispute.";
        action = "Keep relevant documents and consider obtaining qualified legal guidance.";
    }

    // LOW RISK
    else {
        riskLevel = "LOW RISK";
        explanation = "This appears to be a general family-law query.";
        action = "Keep relevant family documents and review the applicable legal information.";
    }
}

    // Property Law
    else if (category === "Property Law") {

    let situationText = situation.toLowerCase();

    // HIGH RISK
    if (
        situationText.includes("illegal occupation") ||
        situationText.includes("forcibly") ||
        situationText.includes("fraud") ||
        situationText.includes("forged") ||
        situationText.includes("threat") ||
        situationText.includes("dispute over possession")
    ) {
        riskLevel = "HIGH RISK";
        explanation = "This situation may involve a serious property-related legal issue.";
        action = "Keep ownership documents and relevant evidence and consider seeking qualified legal guidance.";
    }

    // MEDIUM RISK
    else if (
        situationText.includes("ownership") ||
        situationText.includes("property dispute") ||
        situationText.includes("rent") ||
        situationText.includes("tenant") ||
        situationText.includes("landlord") ||
        situationText.includes("agreement")
    ) {
        riskLevel = "MEDIUM RISK";
        explanation = "This situation may involve a property-related legal dispute.";
        action = "Keep property agreements, receipts and other relevant documents.";
    }

    // LOW RISK
    else {
        riskLevel = "LOW RISK";
        explanation = "This appears to be a general property-law query.";
        action = "Keep your property documents and review the relevant legal information.";
    }
}
    // Consumer Law
    else if (category === "Consumer Law") {

    let situationText = situation.toLowerCase();

    // HIGH RISK
    if (
        situationText.includes("dangerous product") ||
        situationText.includes("injury") ||
        situationText.includes("fraud") ||
        situationText.includes("scam") ||
        situationText.includes("money stolen") ||
        situationText.includes("serious harm")
    ) {
        riskLevel = "HIGH RISK";
        explanation = "This situation may involve a serious consumer-related legal issue.";
        action = "Keep receipts, product records and other evidence and consider seeking qualified legal guidance.";
    }

    // MEDIUM RISK
    else if (
        situationText.includes("defective") ||
        situationText.includes("refund") ||
        situationText.includes("replacement") ||
        situationText.includes("seller") ||
        situationText.includes("complaint") ||
        situationText.includes("warranty")
    ) {
        riskLevel = "MEDIUM RISK";
        explanation = "This situation may involve a consumer-related dispute.";
        action = "Keep your bill, warranty, communication and other purchase documents.";
    }

    // LOW RISK
    else {
        riskLevel = "LOW RISK";
        explanation = "This appears to be a general consumer-law query.";
        action = "Keep your purchase documents and review the relevant consumer information.";
    }
}

    // Employment Law
    else if (category === "Employment Law") {

    let situationText = situation.toLowerCase();

    // HIGH RISK situations
    if (
        situationText.includes("salary") ||
        situationText.includes("wages") ||
        situationText.includes("harassment") ||
        situationText.includes("threat") ||
        situationText.includes("discrimination") ||
        situationText.includes("abuse")
    ) {
        riskLevel = "HIGH RISK";
        explanation = "This situation may involve a serious employment-related legal issue.";
        action = "Keep all employment records and communication and consider seeking qualified legal guidance.";
    }

    // MEDIUM RISK situations
    else if (
        situationText.includes("terminate") ||
        situationText.includes("termination") ||
        situationText.includes("notice") ||
        situationText.includes("leave") ||
        situationText.includes("contract") ||
        situationText.includes("working hours")
    ) {
        riskLevel = "MEDIUM RISK";
        explanation = "This situation may involve an employment-related legal dispute.";
        action = "Keep relevant employment documents and communication records.";
    }

    // LOW RISK situations
    else {
        riskLevel = "LOW RISK";
        explanation = "This appears to be a general employment-related query.";
        action = "Keep your employment documents and review the relevant information.";
    }
}

    // Set icon
    let riskIcon = "";

    if (riskLevel === "HIGH RISK") {
        riskIcon = "🔴";
    }
    else if (riskLevel === "MEDIUM RISK") {
        riskIcon = "🟠";
    }
    else {
        riskIcon = "🟢";
    }

    // Colour the result box according to the risk level
    result.className =
        riskLevel === "HIGH RISK" ? "high-risk" :
        riskLevel === "MEDIUM RISK" ? "medium-risk" : "low-risk";

    // Display result
    result.innerHTML =
        "<h2>Risk Assessment</h2>" +
        "<h3>" + riskIcon + " " + riskLevel + "</h3>" +
        "<p><strong>Category:</strong> " + category + "</p>" +
        "<p><strong>Assessment:</strong> " + explanation + "</p>" +
        "<p><strong>Suggested Action:</strong> " + action + "</p>" +
        "<p><strong>Note:</strong> This is general information and not a substitute for professional legal advice.</p>";
}
