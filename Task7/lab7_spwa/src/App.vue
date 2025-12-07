<template>
  <div id="app">

    <h3>Выберите изображение из файла</h3>
    <input type="file" accept="image/*" @change="loadImage">

    <div v-if="imgSrc">
      <img :src="imgSrc" @load="onImageLoaded"
           style="max-width:800px; display:block; margin:20px 0;" />
    </div>

    <h3>Гистограмма</h3>
    <label>
      <input type="radio" value="value" v-model="mode" /> Значение
    </label>
    <label>
      <input type="radio" value="color" v-model="mode" /> Цвет (CMYK)
    </label>

    <br /><br />

    <canvas ref="histCanvas"
            width="350"
            height="200"
            style="border:1px solid #999;">
    </canvas>

  </div>
</template>



<script>
export default {
  name: "App",

  data() {
    return {
      imgSrc: null,
      mode: "value",
      image: null
    };
  },

  watch: {
    mode() {
      if (this.image) this.drawHistogram();
    }
  },

  methods: {
    loadImage(e) {
      const file = e.target.files[0];
      if (!file) return;
      this.imgSrc = URL.createObjectURL(file);
    },

    onImageLoaded(e) {
      this.image = e.target;
      this.drawHistogram();
    },

    rgbToCmyk(r, g, b) {
      let R = r / 255, G = g / 255, B = b / 255;

      let K = 1 - Math.max(R, G, B);
      //if (K === 1) return { C:0, M:0, Y:0, K:1 };
      K=0

      let C = (1 - R - K) / (1 - K);
      let M = (1 - G - K) / (1 - K);
      let Y = (1 - B - K) / (1 - K);

      return {
        C: Math.round(C * 255),
        M: Math.round(M * 255),
        Y: Math.round(Y * 255),
        K: Math.round(K * 255)
      };
    },

    drawHistogram() {
      const canvas = this.$refs.histCanvas;
      const ctx = canvas.getContext("2d");

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      const tempCanvas = document.createElement("canvas");
      tempCanvas.width = this.image.width;
      tempCanvas.height = this.image.height;
      const tCtx = tempCanvas.getContext("2d");
      tCtx.drawImage(this.image, 0, 0);

      const imgData = tCtx.getImageData(
        0,
        0,
        tempCanvas.width,
        tempCanvas.height
      ).data;

      let histV = new Array(256).fill(0);
      let histC = new Array(256).fill(0);
      let histM = new Array(256).fill(0);
      let histY = new Array(256).fill(0);

      for (let i = 0; i < imgData.length; i += 4) {
        const r = imgData[i];
        const g = imgData[i + 1];
        const b = imgData[i + 2];

        histV[r]++;
        histV[g]++;
        histV[b]++;

        // CMYK
        const cmyk = this.rgbToCmyk(r, g, b);
        histC[cmyk.C]++;
        histM[cmyk.M]++;
        histY[cmyk.Y]++;
      }

      const maxVal = Math.max(...histV, ...histC, ...histM, ...histY);
      const scale = (canvas.height - 15) / maxVal;
      const barW = canvas.width / 256;

      if (this.mode === "value") {
        ctx.fillStyle = "black";
        for (let i = 255; i >= 0; i--) {
          const h = histV[i] * scale;
          ctx.fillRect(i * barW, canvas.height - 15 - h, barW, h);
        }
      } else {
        // C
        ctx.fillStyle = "cyan";
        for (let i = 255; i >= 0; i--) {
          ctx.fillRect(i * barW, canvas.height - 15 - histC[i] * scale, barW, histC[i] * scale);
        }

        // M
        ctx.fillStyle = "magenta";
        for (let i = 255; i >= 0; i--) {
          ctx.fillRect(i * barW, canvas.height - 15 - histM[i] * scale, barW, histM[i] * scale);
        }

        // Y
        ctx.fillStyle = "yellow";
        for (let i = 255; i >= 0; i--) {
          ctx.fillRect(i * barW, canvas.height - 15 - histY[i] * scale, barW, histY[i] * scale);
        }
      }

      // Градиент-направляющая
      const grad = ctx.createLinearGradient(0, 0, canvas.width, 0);
      grad.addColorStop(0, "#000");
      grad.addColorStop(1, "#fff");
      ctx.fillStyle = grad;
      ctx.fillRect(0, canvas.height - 15, canvas.width, 15);
    }
  }
};
</script>



<style>
body {
  margin: 20px;
  font-family: sans-serif;
}
</style>
