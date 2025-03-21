<template>
  <h1>如果您看到此页面，说明发生了错误</h1>
  <p>请联系管理员, email: XXX@XXX.com</p>
  <p>错误信息：{{ activeMainContent }}</p>
</template>

<script>
export default {
  props: {
    activeMainContent: {
      type: String,
      required: true,
    },
  },
}
</script>

<style></style>
