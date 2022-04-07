<template>
    <v-container>
    <h1>List of commands/tools</h1>
    <br>
    <v-simple-table>
    <thead>
      <tr>
        <th class="text-left">Id</th>
        <th class="text-left">Type</th>
        <th class="text-left">Name</th>
        <th class="text-left">Description</th>
        <th class="text-left">Usage</th>
        <th class="text-left">Source/site</th>
        <th class="text-left">CVE</th>
        <th class="text-left">Attack OS</th>
        <th class="text-left">Phase</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="item in items" :key="item.id">
        <td>{{ item.id }}</td>
        <td>{{ item.type }}</td>
        <td>{{ item.activity }}</td>
        <td>{{ item.changes }}</td>
      </tr>
    </tbody>
  </v-simple-table>
</v-container>

</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      items: [],
    };
  },
  methods: {
    getItems() {
      const path = 'http://localhost:5000/api/items';
      axios.get(path, )
        .then((res) => {
          console.log(res);
          this.items = res.data.items;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    this.getItems();
  },
};
</script>
