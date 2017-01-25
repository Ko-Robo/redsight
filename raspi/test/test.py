#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import smbus
import time

# Strawberry Linux社の「MPU-9250」からI2Cでデータを取得するクラス(python 2)
# https://strawberry-linux.com/catalog/items?code=12250
#
# 2016-05-03 Boyaki Machine

# http://qiita.com/boyaki_machine/items/915f7730c737f2a5cc79


class SL_MPU9250:
    # 定数宣言
    REG_PWR_MGMT_1      = 0x6B
    REG_INT_PIN_CFG     = 0x37
    REG_GYRO_CONFIG     = 0x1B
    REG_ACCEL_CONFIG1   = 0x1C
    REG_ACCEL_CONFIG2   = 0x1D

    MAG_MODE_POWERDOWN  = 0         # 磁気センサpower down
    MAG_MODE_SERIAL_1   = 1         # 磁気センサ8Hz連続測定モード
    MAG_MODE_SERIAL_2   = 2         # 磁気センサ100Hz連続測定モード
    MAG_MODE_SINGLE     = 3         # 磁気センサ単発測定モード
    MAG_MODE_EX_TRIGER  = 4         # 磁気センサ外部トリガ測定モード
    MAG_MODE_SELF_TEST  = 5         # 磁気センサセルフテストモード

    MAG_ACCESS          = False     # 磁気センサへのアクセス可否
    MAG_MODE            = 0         # 磁気センサモード
    MAG_BIT             = 14        # 磁気センサが出力するbit数

    offsetRoomTemp      = 0
    tempSensitivity     = 333.87
    gyroRange           = 250       # 'dps' 00:250, 01:500, 10:1000, 11:2000
    accelRange          = 2         # 'g' 00:±2, 01:±4, 10:±8, 11:±16
    magRange            = 4912      # 'μT'  

    offsetAccelX        = 0.0
    offsetAccelY        = 0.0
    offsetAccelZ        = 0.0
    offsetGyroX         = 0.0
    offsetGyroY         = 0.0
    offsetGyroZ         = 0.0

    # コンストラクタ
    def __init__(self, address, channel):
        self.address    = address
        self.channel    = channel
        self.bus        = smbus.SMBus(self.channel)
        self.addrAK8963 = 0x0C

        # Sensor initialization
        self.resetRegister()
        self.powerWakeUp()

        self.gyroCoefficient    = self.gyroRange  / float(0x8000)   # センシングされたDecimal値をdpsに変換する係数
        self.accelCoefficient   = self.accelRange / float(0x8000)   # センシングされたDecimal値をgに変換する係数
        self.magCoefficient16   = self.magRange   / 32760.0         # センシングされたDecimal値をμTに変換する係数(16bit時)
        self.magCoefficient14   = self.magRange   / 8190.0          # センシングされたDecimal値をμTに変換する係数(14bit時)

    # レジスタを初期設定に戻します。
    def resetRegister(self):
        if self.MAG_ACCESS == True:
            self.bus.write_i2c_block_data(self.addrAK8963, 0x0B, [0x01])    
        self.bus.write_i2c_block_data(self.address, 0x6B, [0x80])
        self.MAG_ACCESS = False
        time.sleep(0.1)     

    # レジスタをセンシング可能な状態にします。
    def powerWakeUp(self):
        # PWR_MGMT_1をクリア
        self.bus.write_i2c_block_data(self.address, self.REG_PWR_MGMT_1, [0x00])
        time.sleep(0.1)
        # I2Cで磁気センサ機能(AK8963)へアクセスできるようにする(BYPASS_EN=1)
        self.bus.write_i2c_block_data(self.address, self.REG_INT_PIN_CFG, [0x02])
        self.MAG_ACCESS = True
        time.sleep(0.1)

    # 磁気センサのレジスタを設定する
    def setMagRegister(self, _mode, _bit):      
        if self.MAG_ACCESS == False:
            # 磁気センサへのアクセスが有効になっていないので例外を上げる
            raise Exception('001 Access to a sensor is invalid.')

        _writeData  = 0x00
        # 測定モードの設定
        if _mode=='8Hz':            # 連続測定モード１
            _writeData      = 0x02
            self.MAG_MODE   = self.MAG_MODE_SERIAL_1
        elif _mode=='100Hz':        # 連続測定モード２
            _writeData      = 0x06
            self.MAG_MODE   = self.MAG_MODE_SERIAL_2
        elif _mode=='POWER_DOWN':   # パワーダウンモード
            _writeData      = 0x00
            self.MAG_MODE   = self.MAG_MODE_POWERDOWN
        elif _mode=='EX_TRIGER':    # 外部トリガ測定モード
            _writeData      = 0x04
            self.MAG_MODE   = self.MAG_MODE_EX_TRIGER
        elif _mode=='SELF_TEST':    # セルフテストモード
            _writeData      = 0x08
            self.MAG_MODE   = self.MAG_MODE_SELF_TEST
        else:   # _mode='SINGLE'    # 単発測定モード
            _writeData      = 0x01
            self.MAG_MODE   = self.MAG_MODE_SINGLE

        #　出力するbit数 
        if _bit=='14bit':           # 14bit出力
            _writeData      = _writeData | 0x00
            self.MAG_BIT    = 14
        else:   # _bit='16bit'      # 16bit 出力
            _writeData      = _writeData | 0x10
            self.MAG_BIT    = 16

        self.bus.write_i2c_block_data(self.addrAK8963, 0x0A, [_writeData])

    # 加速度の測定レンジを設定します。広レンジでは測定粒度が荒くなります。
    # val = 16, 8, 4, 2(default)
    def setAccelRange(self, val, _calibration=False):
        # ±2g (00), ±4g (01), ±8g (10), ±16g (11)
        if val==16 :
            self.accelRange     = 16
            _data               = 0x18
        elif val==8 :
            self.accelRange     = 8
            _data               = 0x10
        elif val==4 :
            self.accelRange     = 4
            _data               = 0x08
        else:
            self.accelRange     = 2
            _data               = 0x00

        self.bus.write_i2c_block_data(self.address, self.REG_ACCEL_CONFIG1, [_data])
        self.accelCoefficient   = self.accelRange / float(0x8000)
        time.sleep(0.1)

        # オフセット値をリセット(過去のオフセット値が引き継がれないように)
        self.offsetAccelX       = 0
        self.offsetAccelY       = 0
        self.offsetAccelZ       = 0

        # 本当はCalibrationしたほうが良いと思うけれど、時間もかかるし。
        if _calibration == True:
            self.calibAccel(1000)
        return

    # ジャイロの測定レンジを設定します。広レンジでは測定粒度が荒くなります。
    # val= 2000, 1000, 500, 250(default)
    def setGyroRange(self, val, _calibration=False):
        if val==2000:
            self.gyroRange      = 2000
            _data               = 0x18
        elif val==1000:
            self.gyroRange      = 1000
            _data               = 0x10
        elif val==500:
            self.gyroRange      = 500
            _data               = 0x08
        else:
            self.gyroRange      = 250
            _data               = 0x00

        self.bus.write_i2c_block_data(self.address, self.REG_GYRO_CONFIG, [_data])
        self.gyroCoefficient    = self.gyroRange / float(0x8000)
        time.sleep(0.1)

        # オフセット値をリセット(過去のオフセット値が引き継がれないように)
        self.offsetGyroX        = 0
        self.offsetGyroY        = 0
        self.offsetGyroZ        = 0

        # 本当はCalibrationしたほうが良いのだが、時間もかかるし。
        if _calibration == True:
            self.calibGyro(1000)
        return

    # 加速度センサのLowPassFilterを設定します。
    # def setAccelLowPassFilter(self,val):      

    #センサからのデータはそのまま使おうとするとunsignedとして扱われるため、signedに変換(16ビット限定）
    def u2s(self,unsigneddata):
        if unsigneddata & (0x01 << 15) : 
            return -1 * ((unsigneddata ^ 0xffff) + 1)
        return unsigneddata

    # 加速度値を取得します
    def getAccel(self):
        data    = self.bus.read_i2c_block_data(self.address, 0x3B ,6)
        rawX    = self.accelCoefficient * self.u2s(data[0] << 8 | data[1]) + self.offsetAccelX
        rawY    = self.accelCoefficient * self.u2s(data[2] << 8 | data[3]) + self.offsetAccelY
        rawZ    = self.accelCoefficient * self.u2s(data[4] << 8 | data[5]) + self.offsetAccelZ
        return rawX, rawY, rawZ

    # ジャイロ値を取得します。
    def getGyro(self):
        data    = self.bus.read_i2c_block_data(self.address, 0x43 ,6)
        rawX    = self.gyroCoefficient * self.u2s(data[0] << 8 | data[1]) + self.offsetGyroX
        rawY    = self.gyroCoefficient * self.u2s(data[2] << 8 | data[3]) + self.offsetGyroY
        rawZ    = self.gyroCoefficient * self.u2s(data[4] << 8 | data[5]) + self.offsetGyroZ
        return rawX, rawY, rawZ

    def getMag(self):
        if self.MAG_ACCESS == False:
            # 磁気センサが有効ではない。
            raise Exception('002 Access to a sensor is invalid.')

        # 事前処理
        if self.MAG_MODE==self.MAG_MODE_SINGLE:
            # 単発測定モードは測定終了と同時にPower Downになるので、もう一度モードを変更する
            if self.MAG_BIT==14:                # 14bit出力
                _writeData      = 0x01
            else:                               # 16bit 出力
                _writeData      = 0x11
            self.bus.write_i2c_block_data(self.addrAK8963, 0x0A, [_writeData])
            time.sleep(0.01)

        elif self.MAG_MODE==self.MAG_MODE_SERIAL_1 or self.MAG_MODE==self.MAG_MODE_SERIAL_2:
            status  = self.bus.read_i2c_block_data(self.addrAK8963, 0x02 ,1)
            if (status[0] & 0x02) == 0x02:
                # データオーバーランがあるので再度センシング
                self.bus.read_i2c_block_data(self.addrAK8963, 0x09 ,1)

        elif self.MAG_MODE==self.MAG_MODE_EX_TRIGER:
            # 未実装
            return

        elif self.MAG_MODE==self.MAG_MODE_POWERDOWN:
            raise Exception('003 Mag sensor power down')

        # ST1レジスタを確認してデータ読み出しが可能か確認する。
        status  = self.bus.read_i2c_block_data(self.addrAK8963, 0x02 ,1)
        while (status[0] & 0x01) != 0x01:
            # データレディ状態まで待つ
            time.sleep(0.01)
            status  = self.bus.read_i2c_block_data(self.addrAK8963, 0x02 ,1)

        # データ読み出し
        data    = self.bus.read_i2c_block_data(self.addrAK8963, 0x03 ,7)
        rawX    = self.u2s(data[1] << 8 | data[0])  # 下位bitが先
        rawY    = self.u2s(data[3] << 8 | data[2])  # 下位bitが先
        rawZ    = self.u2s(data[5] << 8 | data[4])  # 下位bitが先
        st2     = data[6]

        # オーバーフローチェック
        if (st2 & 0x08) == 0x08:
            # オーバーフローのため正しい値が得られていない
            raise Exception('004 Mag sensor over flow')

        # μTへの変換
        if self.MAG_BIT==16:    # 16bit出力の時
            rawX    = rawX * self.magCoefficient16
            rawY    = rawY * self.magCoefficient16
            rawZ    = rawZ * self.magCoefficient16
        else:                   # 14bit出力の時
            rawX    = rawX * self.magCoefficient14
            rawY    = rawY * self.magCoefficient14
            rawZ    = rawZ * self.magCoefficient14

        return rawX, rawY, rawZ

    def getTemp(self):
        data    = self.bus.read_i2c_block_data(self.address, 0x65 ,2)
        raw     = data[0] << 8 | data[1]
        return ((raw - self.offsetRoomTemp) / self.tempSensitivity) + 21

    def selfTestMag(self):
        print "start mag sensor self test"
        self.setMagRegister('SELF_TEST','16bit')
        self.bus.write_i2c_block_data(self.addrAK8963, 0x0C, [0x40])
        time.sleep(1.0)
        data = self.getMag()

        print data

        self.bus.write_i2c_block_data(self.addrAK8963, 0x0C, [0x00])
        self.setMagRegister('POWER_DOWN','16bit')
        time.sleep(1.0)
        print "end mag sensor self test"
        return

    # 加速度センサを較正する
    # 本当は緯度、高度、地形なども考慮する必要があるとは思うが、簡略で。
    # z軸方向に正しく重力がかかっており、重力以外の加速度が発生していない前提
    def calibAccel(self, _count=1000):
        print "Accel calibration start"
        _sum    = [0,0,0]

        # 実データのサンプルを取る
        for _i in range(_count):
            _data   = self.getAccel()
            _sum[0] += _data[0]
            _sum[1] += _data[1]
            _sum[2] += _data[2]

        # 平均値をオフセットにする
        self.offsetAccelX   = -1.0 * _sum[0] / _count
        self.offsetAccelY   = -1.0 * _sum[1] / _count
        self.offsetAccelZ   = -1.0 * ((_sum[2] / _count ) - 1.0)    # 重力分を差し引く

        # オフセット値をレジスタに登録したいけれど、動作がわからないので実装保留

        print "Accel calibration complete"
        return self.offsetAccelX, self.offsetAccelY, self.offsetAccelZ

    # ジャイロセンサを較正する
    # 各軸に回転が発生していない前提
    def calibGyro(self, _count=1000):
        print "Gyro calibration start"
        _sum    = [0,0,0]

        # 実データのサンプルを取る
        for _i in range(_count):
            _data   = self.getGyro()
            _sum[0] += _data[0]
            _sum[1] += _data[1]
            _sum[2] += _data[2]

        # 平均値をオフセットにする
        self.offsetGyroX    = -1.0 * _sum[0] / _count
        self.offsetGyroY    = -1.0 * _sum[1] / _count
        self.offsetGyroZ    = -1.0 * _sum[2] / _count

        # オフセット値をレジスタに登録したいけれど、動作がわからないので実装保留

        print "Gyro calibration complete"
        return self.offsetGyroX, self.offsetGyroY, self.offsetGyroZ


if __name__ == "__main__":
    sensor  = SL_MPU9250(0x68,1)
    sensor.resetRegister()
    sensor.powerWakeUp()
    sensor.setAccelRange(8,True)
    sensor.setGyroRange(1000,True)
    sensor.setMagRegister('100Hz','16bit')
    # sensor.selfTestMag()

    while True:
        now     = time.time()
        acc     = sensor.getAccel()
        gyr     = sensor.getGyro()
        mag     = sensor.getMag()
        print "%+8.7f" % acc[0] + " ",
        print "%+8.7f" % acc[1] + " ",
        print "%+8.7f" % acc[2] + " ",
        print " |   ",
        print "%+8.7f" % gyr[0] + " ",
        print "%+8.7f" % gyr[1] + " ",
        print "%+8.7f" % gyr[2] + " ",
        print " |   ",
        print "%+8.7f" % mag[0] + " ",
        print "%+8.7f" % mag[1] + " ",
        print "%+8.7f" % mag[2]

        sleepTime       = 0.1 - (time.time() - now)
        if sleepTime < 0.0:
            continue
        time.sleep(sleepTime)
