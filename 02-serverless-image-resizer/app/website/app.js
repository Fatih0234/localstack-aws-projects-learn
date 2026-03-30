(function ($) {
    let functionUrlPresign = localStorage.getItem("functionUrlPresign");
    if (functionUrlPresign) {
        $("#functionUrlPresign").val(functionUrlPresign);
    }

    let functionUrlList = localStorage.getItem("functionUrlList");
    if (functionUrlList) {
        console.log("function url list is", functionUrlList);
        $("#functionUrlList").val(functionUrlList);
    }

    let functionUrlStyleTransfer = localStorage.getItem("functionUrlStyleTransfer");
    if (functionUrlStyleTransfer) {
        console.log("function url styletransfer is", functionUrlStyleTransfer);
        $("#functionUrlStyleTransfer").val(functionUrlStyleTransfer);
    }

    let imageItemTemplate = Handlebars.compile($("#image-item-template").html());

    $("#configForm").submit(async function (event) {
        if (event.preventDefault)
            event.preventDefault();
        else
            event.returnValue = false;

        event.preventDefault();
        let action = $(this).find("button[type=submit]:focus").attr('name');
        if (action === undefined) {
            // the jquery find with the focus does not work on Safari, maybe because the focus is not instantly given
            // fallback to manually retrieving the submitter from the original event
            action = event.originalEvent.submitter.getAttribute('name')
        }

        if (action == "load") {
            let baseUrl = `${document.location.protocol}//${document.location.host}`;
            if (baseUrl.indexOf("file://") >= 0) {
                baseUrl = `http://localhost:4566`;
            }
            // Convert S3 website URLs to LocalStack endpoint
            baseUrl = baseUrl.replace(/:\/\/.*\.s3-website\./, "://").replace(/:\/\/.*\.s3\./, "://");
            baseUrl = baseUrl.replace(/localhost\.localstack\.cloud:\d+/, "localhost:4566");
            if (!baseUrl.includes("localhost:4566")) {
                baseUrl = `http://localhost:4566`;
            }
            
            console.log("Base URL for API calls:", baseUrl);
            
            const headers = {authorization: "AWS4-HMAC-SHA256 Credential=test/20231004/us-east-1/lambda/aws4_request, ..."};
            const loadUrl = async (funcName, resultElement) => {
                try {
                    const url = `${baseUrl}/2021-10-31/functions/${funcName}/urls`;
                    console.log(`Fetching ${funcName} URL from:`, url);
                    const result = await $.ajax({url, headers}).promise();
                    const funcUrl = JSON.parse(result).FunctionUrlConfigs[0].FunctionUrl;
                    $(`#${resultElement}`).val(funcUrl);
                    localStorage.setItem(resultElement, funcUrl);
                    console.log(`✅ Loaded ${funcName} URL:`, funcUrl);
                } catch (error) {
                    console.error(`❌ Error loading ${funcName} URL:`, error);
                    alert(`Error loading ${funcName} URL. Check console for details.`);
                    throw error;
                }
            }
            await loadUrl("presign", "functionUrlPresign");
            await loadUrl("list", "functionUrlList");
            await loadUrl("styletransfer", "functionUrlStyleTransfer");
            alert("Function URL configurations loaded");
        } else if (action == "save") {
            localStorage.setItem("functionUrlPresign", $("#functionUrlPresign").val());
            localStorage.setItem("functionUrlList", $("#functionUrlList").val());
            localStorage.setItem("functionUrlStyleTransfer", $("#functionUrlStyleTransfer").val());
            alert("Configuration saved");
        } else if (action == "clear") {
            localStorage.removeItem("functionUrlPresign");
            localStorage.removeItem("functionUrlList");
            localStorage.removeItem("functionUrlStyleTransfer");
            $("#functionUrlPresign").val("")
            $("#functionUrlList").val("")
            $("#functionUrlStyleTransfer").val("")
            alert("Configuration cleared");
        } else {
            alert("Unknown action");
        }

    });

    $("#uploadForm").submit(function (event) {
        $("#uploadForm button").addClass('disabled');

        if (event.preventDefault)
            event.preventDefault();
        else
            event.returnValue = false;

        event.preventDefault();

        let fileName = $("#customFile").val().replace(/C:\\fakepath\\/i, '');
        let functionUrlPresign = $("#functionUrlPresign").val();

        // modify the original form
        console.log(fileName, functionUrlPresign);

        let urlToCall = functionUrlPresign + "/" + fileName
        console.log(urlToCall);

        $.ajax({
            url: urlToCall,
            success: function (data) {
                console.log("got pre-signed POST URL", data);

                let fields = data['fields'];

                let formData = new FormData()
                
                Object.entries(fields).forEach(([field, value]) => {
                    formData.append(field, value);
                });

                // the file <input> element, "file" needs to be the last element of the form
                const fileElement = document.querySelector("#customFile");
                formData.append("file", fileElement.files[0]);

                console.log("sending form data", formData);

                $.ajax({
                    type: "POST",
                    url: data['url'],
                    data: formData,
                    processData: false,
                    contentType: false,
                    success: function () {
                        alert("success!");
                        updateImageList();
                    },
                    error: function () {
                        alert("error! check the logs");
                    },
                    complete: function (event) {
                        console.log("done", event);
                        $("#uploadForm button").removeClass('disabled');
                    }
                });
            },
            error: function (e) {
                console.log("error", e);
                alert("error getting pre-signed URL. check the logs!");
                $("#uploadForm button").removeClass('disabled');
            }
        });
    });

    function updateImageList() {
        let listUrl = $("#functionUrlList").val();
        if (!listUrl) {
            alert("Please set the function URL of the list Lambda");
            return
        }

        $.ajax({
            url: listUrl,
            success: function (response) {
                $('#imagesContainer').empty(); // Empty imagesContainer
                response.forEach(function (item) {
                    console.log(item);
                    let cardHtml = imageItemTemplate(item);
                    $("#imagesContainer").append(cardHtml);
                });
                
                // Attach event handlers for style transfer buttons
                attachStyleTransferHandlers();
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log("Error:", textStatus, errorThrown);
                alert("error! check the logs");
            }
        });
    }
    
    function attachStyleTransferHandlers() {
        $(".apply-style-btn").click(function () {
            let imageName = $(this).data("image");
            let style = $(`.style-select[data-image="${imageName}"]`).val();
            
            if (!style) {
                alert("Please select a style first");
                return;
            }
            
            applyStyle(imageName, style, $(this));
        });
    }
    
    function applyStyle(imageName, style, buttonElement) {
        let styleTransferUrl = $("#functionUrlStyleTransfer").val();
        if (!styleTransferUrl) {
            alert("Please set the function URL of the styletransfer Lambda");
            return;
        }
        
        // Disable button and show loading
        buttonElement.prop('disabled', true);
        buttonElement.html('<i class="bi bi-hourglass-split"></i> Processing...');
        
        let statusDiv = $(`.style-status[data-image="${imageName}"]`);
        statusDiv.html('<small class="text-muted">Applying style...</small>');
        
        $.ajax({
            type: "POST",
            url: styleTransferUrl + "/" + imageName,
            contentType: "application/json",
            data: JSON.stringify({ style: style }),
            success: function (response) {
                statusDiv.html('<small class="text-success"><i class="bi bi-check-circle"></i> Style applied!</small>');
                setTimeout(function () {
                    updateImageList(); // Refresh to show styled image
                }, 1500);
            },
            error: function (xhr, status, error) {
                console.log("Style transfer error:", error);
                buttonElement.prop('disabled', false);
                buttonElement.html('<i class="bi bi-magic"></i> Apply');
                let errorMsg = xhr.responseJSON ? xhr.responseJSON.error : error;
                statusDiv.html(`<small class="text-danger"><i class="bi bi-exclamation-triangle"></i> ${errorMsg}</small>`);
            }
        });
    }

    $("#updateImageListButton").click(function (event) {
        updateImageList();
    });

    if (functionUrlList) {
        updateImageList();
    }

})(jQuery);
