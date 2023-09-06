from sqlalchemy import Column, String, Integer, DateTime,ForeignKey
from model import Base

class Operacao(Base):
    __tablename__ = 'operacao'
    id_operacao = Column("id_operacao", Integer, primary_key=True)    
    dt_entrada = Column("dt_entrada",DateTime)
    dt_saida = Column("dt_saida",DateTime)
    id_veiculo = Column("id_veiculo",Integer)
    id_tipo_operacao = Column("id_operacao_tip", Integer,\
                             ForeignKey("tipo_operacao.id_operacao_tip"),
                             nullable=False)


    ## criar o vinculo com os modelos do veiculo
    """ modelos = relationship("Modelo", cascade="all,delete",
                                back_populates="marca")  """
    
    def __init__(self, data_entrada: DateTime,
                codigo_veiculo: Integer,
                codigo_tipo_operacao: Integer):
        """
        Cria uma marca de veiculo

        Argumentos:
            sigla: sigla do tipo de operacao E-EVENTUAL / D-DIARIO / M-MENSAL
        """
        self.dt_entrada= data_entrada
        self.id_veiculo = codigo_veiculo
        self.id_tipo_operacao = codigo_tipo_operacao