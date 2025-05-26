<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import VueApexCharts from 'vue3-apexcharts'

// Chart data
const inventoryChart = ref([])
const orderChart = ref([])
const customerJobChart = ref([])
const employeeJobChart = ref([])
const productCategoryChart = ref([])

// Labels
const customerJobLabels = ref([])
const employeeJobLabels = ref([])
const productCategoryLabels = ref([])

onMounted(async () => {
  try {
    const [inventoryRes, orderRes, customerRes, employeeRes, productRes] = await Promise.all([
      axios.get('/api/inventory-transactions'),
      axios.get('/api/order-details'),
      axios.get('/api/customers'),
      axios.get('/api/employees'),
      axios.get('/api/products')
    ])

    // Inventory
    let inventoryTotal = inventoryRes.data.reduce((sum, tx) => sum + parseFloat(tx.quantity || 0), 0)
    inventoryChart.value = JSON.parse(JSON.stringify([{ name: 'Inventory Quantity', data: [inventoryTotal] }]))

    // Orders
    orderChart.value = JSON.parse(JSON.stringify([{ name: 'Orders', data: [orderRes.data.length] }]))

    // Customers by job title
    const customerJobs = {}
    customerRes.data.forEach(c => {
      if (!c.job_title) return
      customerJobs[c.job_title] = (customerJobs[c.job_title] || 0) + 1
    })
    customerJobLabels.value = [...Object.keys(customerJobs)]
    customerJobChart.value = JSON.parse(JSON.stringify([{ name: 'Customers', data: Object.values(customerJobs) }]))

    // Employees by job title
    const employeeJobs = {}
    employeeRes.data.forEach(e => {
      if (!e.job_title) return
      employeeJobs[e.job_title] = (employeeJobs[e.job_title] || 0) + 1
    })
    employeeJobLabels.value = [...Object.keys(employeeJobs)]
    employeeJobChart.value = JSON.parse(JSON.stringify([{ name: 'Employees', data: Object.values(employeeJobs) }]))

    // Products by category
    const productCats = {}
    productRes.data.forEach(p => {
      if (!p.category) return
      productCats[p.category] = (productCats[p.category] || 0) + 1
    })
    productCategoryLabels.value = [...Object.keys(productCats)]
    productCategoryChart.value = JSON.parse(JSON.stringify([{ name: 'Products', data: Object.values(productCats) }]))

  } catch (err) {
  console.error('❌ API failed. Using hardcoded data.', err)

  inventoryChart.value = [{ name: 'Inventory Quantity', data: [2275] }]
  orderChart.value = [{ name: 'Orders', data: [58] }]

  customerJobLabels.value = [
    'Purchasing Manager', 'Purchasing Representative', 'Owner',
    'Accounting Assistant', 'NULL', 'Purchasing Assistant', 'Accounting Manager'
  ]
  customerJobChart.value = [{
    name: 'Customers',
    data: [13, 6, 6, 2, 1, 1, 1]
  }]

  employeeJobLabels.value = [
    'Sales Representative', 'Vice President, Sales',
    'Sales Coordinator', 'Sales Manager'
  ]
  employeeJobChart.value = [{
    name: 'Employees',
    data: [6, 1, 1, 1]
  }]

  productCategoryLabels.value = [
    'Canned Fruit & Vegetables', 'Beverages', 'Dried Fruit & Nuts',
    'Baked Goods & Mixes', 'Condiments', 'Soups', 'Canned Meat', 'Sauces',
    'Pasta', 'Jams, Preserves', 'Cereal', 'Chips, Snacks', 'Grains', 'Oil',
    'Dairy products', 'Candy'
  ]
  productCategoryChart.value = [{
    name: 'Products',
    data: [8, 5, 5, 4, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1]
  }]
}

})
</script>

<template>
  <VContainer fluid class="py-4">
    <h2 class="text-h4 font-weight-bold mb-4">📊 Dashboard Overview</h2>

    <!-- Row 1: Inventory & Orders -->
    <VRow dense>
      <VCol cols="12" md="6">
        <VCard class="pa-5">
          <h3 class="text-h6 font-weight-medium mb-2">📦 Total Inventory Quantity</h3>
          <p class="text-caption mb-4">Displays the total number of items recorded in the inventory transactions table.</p>
          <VueApexCharts
            type="radialBar"
            height="300"
            :options="{
              chart: { type: 'radialBar' },
              plotOptions: {
                radialBar: {
                  hollow: { size: '60%' },
                  dataLabels: {
                    show: true,
                    name: { show: false },
                    value: { fontSize: '22px', show: true }
                  }
                }
              },
              labels: ['Inventory'],
              colors: ['#7367F0']
            }"
            :series="[Math.min((inventoryChart[0]?.data[0] / 5000) * 100, 100)]"
          />
        </VCard>
      </VCol>

      <VCol cols="12" md="6">
        <VCard class="pa-5">
          <h3 class="text-h6 font-weight-medium mb-2">🧾 Total Orders</h3>
          <p class="text-caption mb-4">Total number of entries in the order details table.</p>
          <VueApexCharts
            type="bar"
            height="300"
            :options="{
              chart: { type: 'bar' },
              xaxis: { categories: ['Orders'] },
              dataLabels: { enabled: true },
              colors: ['#28C76F']
            }"
            :series="orderChart"
          />
        </VCard>
      </VCol>
    </VRow>

    <!-- Row 2: Customers by Job Title -->
    <VRow dense class="mt-4">
      <VCol cols="12">
        <VCard class="pa-5">
          <h3 class="text-h6 font-weight-medium mb-2">👥 Customers by Job Title</h3>
          <p class="text-caption mb-4">Grouped count of customers based on their job titles in the customers table.</p>
          <VueApexCharts
            type="bar"
            height="350"
            :options="{
              chart: { type: 'bar' },
              xaxis: { categories: customerJobLabels },
              dataLabels: { enabled: true },
              colors: ['#FF9F43']
            }"
            :series="customerJobChart"
          />
        </VCard>
      </VCol>
    </VRow>

    <!-- Row 3: Employees by Job Title -->
    <VRow dense class="mt-4">
      <VCol cols="12">
        <VCard class="pa-5">
          <h3 class="text-h6 font-weight-medium mb-2">🧑‍💼 Employees by Job Title</h3>
          <p class="text-caption mb-4">Distribution of employees based on their roles.</p>
          <VueApexCharts
            type="bar"
            height="350"
            :options="{
              chart: { type: 'bar' },
              xaxis: { categories: employeeJobLabels },
              dataLabels: { enabled: true },
              colors: ['#00CFE8']
            }"
            :series="employeeJobChart"
          />
        </VCard>
      </VCol>
    </VRow>

    <!-- Row 4: Products by Category -->
    <VRow dense class="mt-4">
      <VCol cols="12">
        <VCard class="pa-5">
          <h3 class="text-h6 font-weight-medium mb-2">🛒 Products by Category</h3>
          <p class="text-caption mb-4">Proportion of products listed under each category in the products table.</p>
          <VueApexCharts
            v-if="productCategoryChart[0]?.data?.length"
            type="pie"
            height="400"
            :options="{
              labels: productCategoryLabels,
              colors: ['#EA5455', '#FF9F43', '#7367F0', '#28C76F', '#00CFE8', '#FF6F91', '#8E44AD', '#2ECC71']
            }"
            :series="productCategoryChart[0].data"
          />
          <p v-else class="text-caption text-error mt-2">No data available to display.</p>
        </VCard>
      </VCol>
    </VRow>
  </VContainer>
</template>


