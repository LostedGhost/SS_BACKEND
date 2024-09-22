function showError(error) {
    Swal.fire({
        icon: "error",
        title: "Erreur",
        text: error,
        error: null
    });
}

function showSuccess(success) {
    Swal.fire({
        icon: "success",
        title: "Succès",
        text: success,
        error: null
    });
}
function drawChart(id, r, seriesNames, seriesData) {
    (function (factory) {
        typeof define === 'function' && define.amd ? define(factory) :
        factory();
    })(function () { 
        'use strict';
        const {merge: merge} = window._;
        const echartSetOption = (e, t, o, r) => {
            const {breakpoints: a, resize: n} = window.phoenix.utils,
            s = t => {
                Object.keys(t).forEach((o => {
                    window.innerWidth > a[o] && e.setOption(t[o]);
                }));
            }, 
            i = document.body;
            e.setOption(merge(o(), t));
            const c = document.querySelector(".navbar-vertical-toggle");
            c && c.addEventListener("navbar.vertical.toggle", () => {
                e.resize(), r && s(r);
            });
            n(() => {
                e.resize(), r && s(r);
            });
            r && s(r);
            i.addEventListener("clickControl", ({detail: {control: a}}) => {
                "phoenixTheme" === a && e.setOption(window._.merge(o(), t));
                r && s(r);
            });
        };

        const tooltipFormatter = (e, t = "MMM DD") => {
            let o = "";
            e.forEach((e => {
                o += `<div class='ms-1'>
                        <h6 class="text-body-tertiary"><span class="fas fa-circle me-1 fs-10" style="color:${e.borderColor ? e.borderColor : e.color}"></span>
                        ${e.seriesName} : ${"object" == typeof e.value ? e.value[1] : e.value}
                        </h6>
                    </div>`;
            }));
            return `<div>
                        <p class='mb-2 text-body-tertiary'>
                            ${window.dayjs(e[0].axisValue).isValid() ? window.dayjs(e[0].axisValue).format(t) : e[0].axisValue}
                        </p>
                        ${o}
                    </div>`;
        };

        const handleTooltipPosition = ([e,,t,,o]) => {
            if(window.innerWidth <= 540) {
                const r = t.offsetHeight,
                a = {top: e[1] - r - 20};
                return a[e[0] < o.viewSize[0] / 2 ? "left" : "right"] = 5, a;
            }
            return null;
        };

        const stackedLineChartInit = () => {
            const {getColor: o, getData: e} = window.phoenix.utils;
            const t = document.getElementById(id);  // Sélectionner l'élément via l'id passé en argument
            if(t){
                t.innerHTML = "";
                const i = e(t, "echarts"),
                a = window.echarts.init(t);

                // Construction dynamique des séries
                const series = seriesNames.map((name, index) => ({
                    name: name,
                    type: "line",
                    symbolSize: 10,
                    itemStyle: {
                        color: o("body-highlight-bg"),
                        borderColor: o(index % 2 === 0 ? "info" : "success"),  // Alternance des couleurs pour l'exemple
                        borderWidth: 2
                    },
                    lineStyle: { color: o(index % 2 === 0 ? "info" : "success") },
                    symbol: "circle",
                    stack: "product",
                    data: seriesData[index]
                }));

                echartSetOption(a, i, () => ({
                    tooltip: {
                        trigger: "axis",
                        padding: [7, 10],
                        backgroundColor: o("body-highlight-bg"),
                        borderColor: o("border-color"),
                        textStyle: {color: o("light-text-emphasis")},
                        borderWidth: 1,
                        transitionDuration: 0,
                        axisPointer: {type: "none"},
                        position: (...o) => handleTooltipPosition(o),
                        formatter: o => tooltipFormatter(o)
                    },
                    xAxis: {
                        type: "category",
                        data: r,  // Utilisation de la liste r passée en argument
                        boundaryGap: !1,
                        axisLine: {lineStyle: {color: o("tertiary-bg"), type: "solid"}},
                        axisTick: {show: !1},
                        axisLabel: {color: o("quaternary-color"), margin: 15, formatter: o => o.substring(0, 3)},
                        splitLine: {show: !1}
                    },
                    yAxis: {
                        type: "value",
                        splitLine: {lineStyle: {color: o("secondary-bg"), type: "dashed"}},
                        boundaryGap: !1,
                        axisLabel: {show: !0, color: o("quaternary-color"), margin: 15},
                        axisTick: {show: !1},
                        axisLine: {show: !1}
                    },
                    series: series,  // Séries construites dynamiquement
                    grid: {right: 10, left: 5, bottom: 5, top: 8, containLabel: !0}
                }));
            }
        };
        
        const {docReady: docReady} = window.phoenix.utils;
        docReady(stackedLineChartInit);
    });
}


app = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            constante: 'Poids',
            valeur: '',
            option: 0,
        }
    },
    methods: {
        enregistrer(){
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
            axios.get('/api/constanteAdd?constante='+this.constante+'&valeur='+this.valeur)
            .then(response => {
                if (response.data.status == 200){
                    showSuccess(response.data.message);
                }
                else{
                    showError(response.data.message);
                }
            })
        }
    },
    mounted() {
        drawChart(
            'graphe', 
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            ["Matcha Latte", "Milk Tea", "Cheese Cocoa"],
            [
                [120, 132, 101, 134, 90, 230, 210],
                [220, 182, 191, 234, 290, 330, 310],
                [150, 232, 201, 154, 190, 330, 410]
            ]
        );        
    },
})
if (document.getElementById("dashboard")){
    app.mount("#dashboard")
}
