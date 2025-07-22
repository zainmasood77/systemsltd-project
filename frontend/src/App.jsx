import React from 'react';
import { useForm } from 'react-hook-form';
import axios from 'axios';

const App = () => {
  const { register, handleSubmit, formState: { errors } } = useForm();

  const onSubmit = async (data) => {
    try {
      await axios.post('http://localhost:5000/schedule', data);
      alert('Schedule created successfully!');
    } catch (err) {
      console.error(err);
      alert('Error creating schedule');
    }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.heading}>API Call Scheduler</h2>
      <form onSubmit={handleSubmit(onSubmit)} style={styles.form}>
        <div style={styles.inputGroup}>
          <label style={styles.label}>Duration (minutes):</label>
          <input type="number" {...register("duration", { required: true })} style={styles.input} />
          {errors.duration && <span style={styles.error}>This field is required</span>}
        </div>

        <div style={styles.inputGroup}>
          <label style={styles.label}>Frequency (calls/hour):</label>
          <input type="number" {...register("frequency", { required: true })} style={styles.input} />
          {errors.frequency && <span style={styles.error}>This field is required</span>}
        </div>

        <div style={styles.inputGroup}>
          <label style={styles.label}>API Endpoint URL:</label>
          <input type="text" {...register("endpoint", { required: true })} style={styles.input} />
          {errors.endpoint && <span style={styles.error}>This field is required</span>}
        </div>

        <button type="submit" style={styles.button}>Submit</button>
      </form>
    </div>
  );
};

const styles = {
  container: {
    maxWidth: '500px',
    margin: '3rem auto',
    padding: '2rem',
    borderRadius: '12px',
    backgroundColor: '#f7f9fc',
    boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
    fontFamily: 'Arial, sans-serif',
  },
  heading: {
    textAlign: 'center',
    marginBottom: '1.5rem',
    color: '#1a202c',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '1.2rem',
  },
  inputGroup: {
    display: 'flex',
    flexDirection: 'column',
  },
  label: {
    marginBottom: '0.5rem',
    color: '#4a5568',
    fontWeight: 'bold',
  },
  input: {
    padding: '0.5rem 0.8rem',
    fontSize: '1rem',
    borderRadius: '6px',
    border: '1px solid #cbd5e0',
  },
  error: {
    color: 'red',
    fontSize: '0.85rem',
    marginTop: '0.3rem',
  },
  button: {
    backgroundColor: '#3182ce',
    color: '#fff',
    padding: '0.8rem',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '1rem',
    fontWeight: 'bold',
    transition: 'background-color 0.3s ease',
  },
};

export default App;