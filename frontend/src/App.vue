<template>
  <v-app>
    <v-toolbar max-height=5% dark class="blue accent-4">
      <v-toolbar-title class="headline text-uppercase">
        <span>LeutMesiene &nbsp;</span>
        <span class="font-weight-light">Hacker Cheatsheet</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn
        href="https://github.com/mauritsmaas/LeutMesiene"
      >
        <span class="mr-2">Latest Release</span>
      </v-btn>
    </v-toolbar>

    <v-content>
      <router-view />
    </v-content>
  </v-app>
</template>



<script>
export default {
  name: 'App'
}
</script>

<style>
</style>
