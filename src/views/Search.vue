<template>
  <div class="search">
    <h1>관리자 - 사용자 정보 검색</h1>
    <form class="search-container">
        <input type="text" id="search-bar" placeholder="enter keywords">
        <a href="#"><img class="search-icon" src="http://www.endlessicons.com/wp-content/uploads/2012/12/search-icon.png"></a>
    </form>
  </div>
</template>

<script>
    export default {
        name: 'Search',
        data() {
          return {}
        },
        mounted() {
            if(!this.$parent.authenticated) {
                this.$router.replace({ name: "Login" });
            }
        },
        methods: {
        }
    }
</script>

<style>
  h1 {
  text-align: center;
  padding: 1em 0;
  }
        
  .search-container{
  width: 490px;
  display: block;
  margin: 0 auto;
  }

  input#search-bar{
  margin: 0 auto;
  width: 100%;
  height: 45px;
  padding: 0 20px;
  font-size: 1rem;
  border: 1px solid #D0CFCE;
  outline: none;
  border: 1px solid #008ABF;
  transition: 0.35s ease;
  color: #008ABF;
  }

  .-webkit-input-placeholder{
  transition: opacity 0.45s ease; 
  opacity: 0;
  }
  
  .-moz-placeholder {
  transition: opacity 0.45s ease; 
  opacity: 0;
  }
  
  .-ms-placeholder {
  transition: opacity 0.45s ease; 
  opacity: 0;
  }    

  .search-icon{
  position: relative;
  float: right;
  width: 75px;
  height: 75px;
  top: -62px;
  right: -45px;
  }
</style>