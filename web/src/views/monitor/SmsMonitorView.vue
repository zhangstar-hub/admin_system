<template>
  <el-card>
    <div class="toolbar-container">
      <div class="toolbar">
        <div class="datetime-picker">
          <el-date-picker
            v-model="time_span"
            type="datetimerange"
            :shortcuts="shortcuts"
            range-separator="To"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            format="YYYY/MM/DD hh:mm"
            value-format="YYYY-MM-DD hh:mm"
            :disabled-date="disabledDate"
          />
        </div>
        <el-button type="primary" @click="refreshData">刷新</el-button>
      </div>
    </div>
    <div class="line-chart" ref="lineChart"></div>
  </el-card>
  <el-card>
    <el-text type="info" size="small" style="padding-left: 5px">
      下一次刷新时间:<span v-text="nexfFlushTime"></span
    ></el-text>
    <div class="line-chart" ref="liveLineChart"></div>
  </el-card>
  <div></div>
</template>

<script setup>
import { ref, onMounted, reactive, onUnmounted } from "vue";
import * as echarts from "echarts";
import monitorApi from "@/api/monitor";

const smsData = reactive({
  dates: [],
  successValues: [],
  failedValues: [],
});
const liveSmsData = reactive({
  dates: [],
  successValues: [],
  failedValues: [],
});

const nexfFlushTime = ref(0);
const lineChart = ref(null);
const liveLineChart = ref(null);
var chart = undefined;
var liveChart = undefined;
const time_span = ref([]);

function disabledDate(time) {
  let yearFirst = new Date();
  yearFirst.setDate(0);
  yearFirst.setMonth(0);
  let yearLast = new Date();
  yearLast.setFullYear(yearLast.getFullYear() + 1); // 设置到明年
  yearLast.setMonth(0); // 明年的0月，也就是对应到1月，是存在的哦，不是不存在的0
  yearLast.setDate(0); // 明年的0日
  return time < yearFirst || time >= yearLast;
}
var keepalive = undefined;

const shortcuts = [
  {
    text: "近一小时",
    value: () => {
      const end = new Date();
      const start = new Date();
      start.setTime(start.getTime() - 3600 * 1000);
      return [start, end];
    },
  },
  {
    text: "近一天",
    value: () => {
      const end = new Date();
      const start = new Date();
      start.setTime(start.getTime() - 3600 * 1000 * 24);
      return [start, end];
    },
  },
  {
    text: "近一周",
    value: () => {
      const end = new Date();
      const start = new Date();
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
      return [start, end];
    },
  },
  {
    text: "近一月",
    value: () => {
      const end = new Date();
      const start = new Date();
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
      return [start, end];
    },
  },
  {
    text: "近三月",
    value: () => {
      const end = new Date();
      const start = new Date();
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
      return [start, end];
    },
  },
];

onMounted(() => {
  chart = echarts.init(lineChart.value);
  let option = {
    legend: {
      data: ["发送成功", "发送失败"],
    },
    title: {
      text: "短信发送情况",
    },
    tooltip: {
      trigger: "axis",
    },
    xAxis: {
      type: "category",
      data: smsData.dates,
    },
    yAxis: {
      type: "value",
    },
    series: [
      {
        name: "发送成功",
        type: "line",
        smooth: true,
        data: smsData.successValues,
      },
      {
        name: "发送失败",
        type: "line",
        color: "red",
        smooth: true,
        data: smsData.failedValues,
      },
    ],
  };
  chart.setOption(option);
  refreshData();

  liveChart = echarts.init(liveLineChart.value);
  let liveOption = {
    legend: {
      data: ["发送成功", "发送失败"],
    },
    title: {
      text: "实时发送情况",
    },
    tooltip: {
      trigger: "axis",
    },
    xAxis: {
      type: "category",
      data: liveSmsData.dates,
    },
    yAxis: {
      type: "value",
    },
    series: [
      {
        name: "发送成功",
        type: "line",
        smooth: true,
        data: liveSmsData.successValues,
      },
      {
        name: "发送失败",
        type: "line",
        color: "red",
        smooth: true,
        data: liveSmsData.failedValues,
      },
    ],
  };
  liveChart.setOption(liveOption);
  keepalive = setInterval(() => {
    nexfFlushTime.value -= 1;
    if (nexfFlushTime.value > 0) return;
    nexfFlushTime.value = 10;
    refreshLiveData();
  }, 1000);
});

onUnmounted(() => {
  clearInterval(keepalive);
});

function refreshLiveData() {
  let end = new Date();
  let start = new Date();
  start.setTime(start.getTime() - 3600 * 1000);
  let params = {
    left_time: start,
    right_time: end,
  };
  monitorApi.smsMonitor(params).then(({ data }) => {
    liveSmsData.dates = data.datetime_span;
    liveSmsData.successValues = data.data.map((e) => e.success);
    liveSmsData.failedValues = data.data.map((e) => e.failed);
    let option = {
      xAxis: {
        data: liveSmsData.dates,
      },
      series: [
        {
          name: "发送成功",
          type: "line",
          smooth: true,
          data: liveSmsData.successValues,
        },
        {
          name: "发送失败",
          type: "line",
          color: "red",
          smooth: true,
          data: liveSmsData.failedValues,
        },
      ],
    };
    liveChart.setOption(option);
  });
}

function refreshData() {
  let params = {
    left_time: time_span.value[0],
    right_time: time_span.value[1],
  };
  chart.showLoading();
  monitorApi.smsMonitor(params).then(({ data }) => {
    smsData.dates = data.datetime_span;
    smsData.successValues = data.data.map((e) => e.success);
    smsData.failedValues = data.data.map((e) => e.failed);
    let option = {
      xAxis: {
        data: smsData.dates,
      },
      series: [
        {
          name: "发送成功",
          type: "line",
          smooth: true,
          data: smsData.successValues,
        },
        {
          name: "发送失败",
          type: "line",
          color: "red",
          smooth: true,
          data: smsData.failedValues,
        },
      ],
    };
    chart.setOption(option);
    chart.hideLoading();
  });
}
</script>

<style scoped lang="scss">
.toolbar-container {
  width: 100%;
  height: 80px;
  .toolbar {
    display: flex;
    flex-wrap: wrap;
    align-items: stretch;
  }
}

.line-chart {
  width: 100%;
  height: 400px;
}
</style>
