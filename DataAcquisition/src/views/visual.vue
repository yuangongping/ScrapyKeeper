<template>
 <div class="visual">
  <a id="gotovisual" href="http://172.16.119.6:5000/visual#" target="_blank" ></a>
</div>
</template>
<script>
export default {
  mounted() {
    document.getElementById('gotovisual').click()
    // const visualUrl = process.env.BACKEND_URL + '/visual';
    // // window.location = visualUrl
  }
}
</script>