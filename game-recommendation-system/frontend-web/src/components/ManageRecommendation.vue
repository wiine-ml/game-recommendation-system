<template>
  <div class="outer-box">
    <h1>推荐参数设置</h1>

    <hr />

    <div class="div-1">
      <h2>算法设置</h2>

      <div class="group">
        <h3>相似度算法设置：</h3>
        <el-radio-group v-model="method_1">
          <el-radio value="cosine" size="large" border>余弦相似度算法</el-radio>
          <el-radio value="iuf" size="large" border>Iuf改进余弦相似度算法</el-radio>
        </el-radio-group>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      method_1: '',
    }
  },
  mounted() {
    this.method_1 = 'cosine'
  },
}
</script>

<style scoped>
.div-1 {
  padding: 20px;
  border-radius: 20px;
  background-color: var(--primary-color);
}

.group {
  display: flex;
  flex-direction: row;
  text-align: center;
  justify-content: center;
}
</style>
