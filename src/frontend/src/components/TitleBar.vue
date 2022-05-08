<template>
  <div class="title-bar mt-3">
      <h2 class="p-3 text-white font-weight-bold text-capitalize">{{ title}}</h2>
  </div>
</template>
<script>
  export default  {
      name: 'TitleBar',
      props: {
        title: String
      }
  }

</script>
<style scoped>
  .title-bar {
      border-top-right-radius: 10px;
      border-top-left-radius: 10px;
      background-color: #25C9D0;
  }
  h2 {
      font-size: 20px;
  }
</style>
