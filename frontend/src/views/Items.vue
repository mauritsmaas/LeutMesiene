<template>
    <v-container>
    <h1>List of commands/tools</h1>
    <br>
    <v-simple-table>
    <thead>
      <tr>
        <th class="text-left">Id</th>
        <th class="text-left">Name</th>
        <th class="text-left">Type</th>
        <th class="text-left">Description</th>
        <th class="text-left">Usage</th>
        <th class="text-left">Source/site</th>
        <th class="text-left">CVE</th>
        <th class="text-left">Attack OS</th>
        <th class="text-left">Phase</th>
      </tr>
    </thead>
    <tbody  v-for="item in items" :key="item.id">
      <tr class="clickable-row" v-on:click="clickItem(item)">
        <td>{{ item.id }}</td>
        <td>{{ item.name }}</td>
        <td>{{ item.type }}</td>
        <td>{{ item.description }}</td>
        <td>{{ item.usage }}</td>
        <td>{{ item.source }}</td>
        <td>{{ item.cve }}</td>
        <td>{{ item.attackos }}</td>
        <td>{{ item.phase }}</td>
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
      const path = 'http://127.0.0.1:5001/api/items';
      axios.get(path, )
        .then((res) => {
          //console.log(res.data.items);
          this.items = res.data.items;
          console.log(this.items)
        })
        .catch((error) => {
          console.error(error);
        });
    },
    clickItem(item) {
      console.log("Click Item fired with " + item.id);
      this.$router.push({ name: "item-details", params: { id: item.id } });
    }
  },
  created() {
    this.getItems();
  },
};
</script>
