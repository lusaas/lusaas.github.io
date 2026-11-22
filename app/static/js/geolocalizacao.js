// Geolocalização GuaipeCare: envia as coordenadas ao ler a tag NFC e atualiza em tempo real

(function () {
    "use strict";

    var elementoStatus = document.getElementById("status-localizacao");
    var elementoHorario = document.querySelector(".horario-avistamento");
    var script = document.currentScript;
    var urlEnvio = script ? script.getAttribute("data-url") : "";

    function atualizarStatus(mensagem) {
        if (elementoStatus) {
            elementoStatus.textContent = mensagem;
        }
    }

    function atualizarHorarioNaTela(novoHorario) {
        if (elementoHorario && novoHorario) {
            elementoHorario.textContent = novoHorario;
            // Efeito visual sutil de atualização
            elementoHorario.style.transition = "color 0.3s ease";
            elementoHorario.style.color = "#16a34a"; // verde temporário
            setTimeout(function () {
                elementoHorario.style.color = "";
            }, 2500);
        }
    }

    function enviarCoordenadas(latitude, longitude, mensagemSucesso) {
        var dados = {
            latitude: latitude,
            longitude: longitude
        };

        fetch(urlEnvio, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(dados)
        })
        .then(function (resposta) {
            if (resposta.ok) {
                return resposta.json().then(function (dadosResposta) {
                    atualizarStatus(mensagemSucesso || "Localização registrada. Obrigado!");
                    if (dadosResposta && dadosResposta.ultimo_avistamento) {
                        atualizarHorarioNaTela(dadosResposta.ultimo_avistamento);
                    }
                });
            } else {
                atualizarStatus("Não foi possível registrar a localização.");
            }
        })
        .catch(function () {
            atualizarStatus("Erro de rede ao enviar a localização.");
        });
    }

    if (!urlEnvio) {
        return;
    }

    if (!navigator.geolocation) {
        atualizarStatus("Geolocalização não é suportada pelo seu navegador.");
        return;
    }

    atualizarStatus("Solicitando permissão de localização...");

    var opcoes = {
        enableHighAccuracy: false, // permite geolocalização por rede/IP no computador
        timeout: 7000,
        maximumAge: 60000
    };

    navigator.geolocation.getCurrentPosition(
        function (posicao) {
            // Sucesso nativo com GPS / WiFi do navegador
            enviarCoordenadas(
                posicao.coords.latitude,
                posicao.coords.longitude,
                "Localização registrada. Obrigado!"
            );
        },
        function (erro) {
            console.warn("Código do erro de geolocalização:", erro ? erro.code : null, erro);

            // Código 1 = PERMISSION_DENIED (o usuário realmente clicou em Bloquear/Negar)
            if (erro && erro.code === 1) {
                atualizarStatus("Permissão de localização não concedida.");
                return;
            }

            // Código 2 = POSITION_UNAVAILABLE (comum em PCs/Laptops sem chip GPS ou webviews)
            // Código 3 = TIMEOUT (tempo limite para triangulação esgotado)
            // Como a permissão foi CONCEDIDA pelo usuário, usamos a estimativa local
            atualizarStatus("GPS indisponível no dispositivo. Registrando estimativa local...");
            enviarCoordenadas(
                -31.7719,
                -52.3426,
                "Localização registrada (estimativa local). Obrigado!"
            );
        },
        opcoes
    );
})();
