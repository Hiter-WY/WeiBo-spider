<template>
  <ContantBase>
    <div class="chart-wrapper">
      <div class="chart-left">
        <Bar :data="chartData" :options="barOptions" />
      </div>
      <div class="chart-right">
        <Pie :data="chartData" :options="pieOptions" />
      </div>
    </div>
  </ContantBase>
</template>

<script>
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale, Tooltip, Legend, ArcElement } from "chart.js";
import { Pie, Bar } from "vue-chartjs";
import { mapState } from "vuex";

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend, ArcElement);

const pieOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right',
      align: 'center',
    },
  },
};

const barOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false,
    },
  },
  scales: {
    x: {
      beginAtZero: true,
    },
    y: {
      beginAtZero: true,
    },
  },
};

export default {
  components: {
    Pie,
    Bar,
  },
  computed: {
    ...mapState({
      count: (state) => state.count,
    }),
    chartData() {
      return {
        labels: [
          "体育",
          "娱乐",
          "家居",
          "房产",
          "教育",
          "时尚",
          "时政",
          "游戏",
          "科技",
          "财经",
        ],
        datasets: [
          {
            label: '分类数量',
            backgroundColor: [
              "#FF6384", // 体育 - 红色
              "#36A2EB", // 娱乐 - 蓝色
              "#FFCE56", // 家居 - 黄色
              "#4BC0C0", // 房产 - 青色
              "#9966FF", // 教育 - 紫色
              "#FF9F40", // 时尚 - 橙色
              "#E7E9ED", // 时政 - 灰色
              "#A2EB36", // 游戏 - 绿色
              "#C9CBCF", // 科技 - 银色
              "#8B4513", // 财经 - 棕色
            ],
            data: [
              this.count["体育"],
              this.count["娱乐"],
              this.count["家居"],
              this.count["房产"],
              this.count["教育"],
              this.count["时尚"],
              this.count["时政"],
              this.count["游戏"],
              this.count["科技"],
              this.count["财经"],
            ],
          },
        ],
      };
    },
  },
  data() {
    return {
      pieOptions,
      barOptions,
    };
  },
};
</script>

<style scoped>
.chart-wrapper {
  display: flex;
  width: 100%;
  height: 500px; /* 可以根据需要调整整体高度 */
}

.chart-left {
  width: 50%;
  padding: 10px; /* 给柱状图和饼图一点间距 */
}

.chart-right {
  width: 50%;
  padding: 10px;
}
</style>
