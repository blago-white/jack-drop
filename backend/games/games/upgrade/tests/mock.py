class ShiftServiceMock:
    _mock_shift_value = 10

    def get(self):
        return self._mock_shift_value
